from . import http_server
from . import ws_server

def get_ip():
	import socket
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		# doesn't even have to be reachable
		s.connect(('10.255.255.255', 1))
		IP = s.getsockname()[0]
	except Exception:
		IP = '127.0.0.1'
	finally:
		s.close()
	return IP


def start():
	ws_server.start()
	http_server.start()
	print("[DISPLAY SERVER] Started, ip:{} | http port:{} | ws port: {}".format(get_ip(), http_server.PORT, ws_server.PORT))

def stop():
	ws_server.close()
	http_server.close()