from channels import Channel
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
import json
from models import Room


@channel_session_user_from_http
def ws_connect(message):
	print 'websocket connect'
	message.reply_channel.send({'accept': True})
	message.channel_session['rooms'] = []


@channel_session_user
def ws_receive(message):
	print 'websocket receive'
	payload = json.loads(message['text'])
	payload['reply_channel'] = message['reply_channel']

	assert 'command' in payload, 'command required in payload: %s'%payload.keys()
	assert 'room' in payload, 'room field required in payload: %s'%payload.keys()
	print payload

	Channel('chat.receive').send(payload)


@channel_session
def ws_disconnect(message):
	print 'websocket disconnect, session had ', message.channel_session['rooms']

	for room_id in message.channel_session['rooms']:
		try:
			room = Room.objects.get(pk=room_id)
			print 'trying to remove disconnecting user from ', room
			payload = {
				'reply_channel': message['reply_channel'],
				'command': 'leave',
				'room': room.title
			}
			Channel('chat.receive').send(payload)
		except Room.DoesNotExist:
			print 'room does not exist'
			pass  # no group to remove them from
