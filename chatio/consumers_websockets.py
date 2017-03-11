from channels import Channel
from channels.auth import channel_session_user, channel_session_user_from_http
import json


@channel_session_user_from_http
def ws_connect(message):
	print 'websocket connect'
	message.reply_channel.send({'accept': True})


@channel_session_user
def ws_receive(message):
	print 'websocket receive'
	payload = json.loads(message['text'])
	payload['reply_channel'] = message['reply_channel']

	assert 'command' in payload, 'command field reuired in payload'
	assert 'room' in payload, 'room field required in payload'
	print payload

	Channel('chat.receive').send(payload)
