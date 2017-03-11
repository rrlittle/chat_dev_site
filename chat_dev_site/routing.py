from channels.routing import include

channel_routing = [
	include('chatio.routing.channel_routes'),
	include('chatio.routing.websocket_routes', path=r'^/chat'),
]
