from channels import route
import consumers_channels as ch
import consumers_websockets as ws

channel_routes = [
	route('chat.receive', ch.chat_create_room, command=r'^create$'),
	route('chat.receive', ch.chat_join, command=r'^join$'),
	route('chat.receive', ch.chat_leave, command=r'^leave$'),
	route('chat.receive', ch.chat_send, command=r'^send$'),
]

websocket_routes = [
	route('websocket.connect', ws.ws_connect),
	route('websocket.receive', ws.ws_receive),
	# route('websocket.disconnect', ws.ws_disconnect),
]
