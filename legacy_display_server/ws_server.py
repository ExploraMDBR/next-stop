from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import json
from datetime import datetime
import threading
# import re
from sys import stdout
# __TEMP_condition = threading.Condition()
# __TEMP_user_creation = 0

PORT = 8001
clients = []

def get_comm_json(msg, state="system"):
	return json.dumps({
		"state": state,
		"msg": msg,
		"count": 0
		})

def dump_to_console(msg, xtra=None):
	print("[WS] {} | xtra arg: {}".format(msg, xtra))
	stdout.flush()


class Explora_Websocket_Handler(WebSocket):
	def handleMessage(self):
		dump_to_console("incoming MSG: {}".format(self.data))

	def handleConnected(self):
		clients.append(self)
		self.sendMessage(
			get_comm_json("Pari WS server: UP (%d clients connected)")
			% len(clients)
		)
		dump_to_console(
			"Client connected: ({}:{}), total {} clients".format(
				self.address[0], self.address[1], len(clients)
			)
		)

	def handleClose(self):
		dump_to_console(
			"[Client removed: ({}:{}), total {} clients".format(
				self.address[0], self.address[1], len(clients)
			)
		)
		clients.remove(self)
		
def send(content):
	for c in clients:
		c.sendMessage(content)

_ws_server = None

def serveforever():
	global _ws_server
	_ws_server = SimpleWebSocketServer("", PORT, Explora_Websocket_Handler)
	try:
		_ws_server.serveforever()
	except ValueError as e:
		pass

t = threading.Thread(target = serveforever)

def start():
	t.start()


def close():
	if _ws_server:
		_ws_server.close()
	if t.is_alive():
		t.join()

