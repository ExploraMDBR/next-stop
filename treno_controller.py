from explora.hat import gpio_manager
import legacy_display_server

import threading
from time import sleep, time

btns = gpio_manager.Button_Manager(extra_btn = True)
leds = gpio_manager.leds[:5]
train_rails = gpio_manager.leds[5]

STATE_STR = [ "CHIAVE", "PANTOGRAFO", "RADIO", "PORTE", "QUALCOSA", "ARMED", "RUNNING", "IDLE"]
state = len(STATE_STR) - 1 #IDLE
TRENO_RUNNING_TIME = 4
auto_control_running = False
FLASH_OTHER_LEDS = False
STATE_TIMEOUT = 1
_last_state_change = time()
_state_set_by_button = False
_keep_watchdog = True

def timeout_state():
	global state, _state_set_by_button, auto_control_running, _last_state_change
	# print("WATCHDOG START", _state_set_by_button, auto_control_running)

	while  _keep_watchdog:
		# print("WATCHDOG loop", _state_set_by_button, auto_control_running)
		sleep(0.1)
		if not _state_set_by_button or auto_control_running:
			continue
		
		now = time()
		print("WATCHDOG INTERVAL", now - _last_state_change)
		if now - _last_state_change > STATE_TIMEOUT:
			_last_state_change = now
			_state_set_by_button = False
			state = len(STATE_STR) - 1 #IDLE
			light_state_leds()
			send_ws_state()
			print("WATCHDOG STATE CHANGE", state)
		
watchdog_thread = threading.Thread(target = timeout_state)

def get_state(num):
	return STATE_STR[num]

def send_ws_state():
	display_server.ws_server.send(legacy_display_server.ws_server.get_comm_json("treno button", get_state(state)))

def set_state(num_or_str):
	global state
	if isinstance(num_or_str, (int)):
		state = num_or_str
	elif isinstance(num_or_str, str):
		state = STATE_STR.index(num_or_str)
	else:
		raise TypeError("only int or str allowed to set state")

def light_led(num, the_led):
	for led in leds:
		led.off()

	the_led.on()

def light_state_leds():
	global state
	light = []
	for i, led in enumerate(leds):
		if get_state(state) in ("RUNNING", "IDLE") or i > state:
			led.off()
		else:
			led.on()
			light.append(i)
	# print("leds {} on | state {}".format(light, state))


def control_train(run):
	if run:
		train_rails.on()
	else:
		train_rails.off()



def auto_control_state():
	global auto_control_running
	if auto_control_running:
		return
	auto_control_running = True


	control_train(True)
	counter = 0
	led_time = 0.2
	for blink in range(int(TRENO_RUNNING_TIME / led_time)):
		light_led(counter%5, leds[counter%5])
		counter +=1
		sleep(led_time)

	set_state("IDLE")
	_last_state_change = time()
	send_ws_state()
	light_state_leds()
	control_train(False)
	print("auto", get_state(state), state)
	auto_control_running = False


def move_state(num, the_led):
	global state, _state_set_by_button, _last_state_change
	looping_state = (state + 1) % len(STATE_STR)
	_last_state_change = time()
	_state_set_by_button = True
	# print("STATE CHANGE BY BUTTON", _state_set_by_button)
	
	if num == looping_state:
		state = num 
		send_ws_state()
		print("ok  btn={} state={}".format(num , looping_state), get_state(state))

	else:
		if FLASH_OTHER_LEDS:
			for led in leds:
				led.on()
			sleep(0.5)
			for led in leds:
				led.off()

	light_state_leds()
 
	if get_state(state) == "RUNNING":
		# t = threading.Thread(target = auto_control_state())
		# t.start()
		auto_control_state()

		# print("auto  btn={} state={}".format(num , looping_state), get_state(state))
		# sleep(1)
		# set_state("IDLE")
		# light_state_leds()
		# print("auto  btn={} state={}".format(num , looping_state), get_state(state))


if __name__ == '__main__':
	watchdog_thread.start()
	
	legacy_display_server.start()

	for i in range(7):
		btns.set_press_handler(i, move_state)

	try:
		input("Press enter to end")
	finally:
		_keep_watchdog = False
		legacy_display_server.stop()
		watchdog_thread.join()
		print("exit")
	
