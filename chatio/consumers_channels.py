from channels import Channel
from models import Message, Room
from channels.auth import channel_session_user
import json
from settings import CHATIO_ALLOW_ROOM_CREATION


def chat_create_room(chan_msg):
	''' if the room doesn't exist create it. then pass the msg onto chat_join
	'''

	try:
		# see if room exists
		Room.objects.get(title=chan_msg['room'])
	except Room.DoesNotExist:
		# if the setting don't allow clients to create chatrooms
		if not CHATIO_ALLOW_ROOM_CREATION: 
			chan_msg.reply_channel.send({
				'text': json.dumps({
					'err': ('clients not allowed to create chatrooms.'
										'and room doesn not exist')
				})
			})
			return
		else:
			# create the room
			Room.objects.create(title=chan_msg['room']).save()
			print 'creating room %s'%chan_msg['room']
	finally:
		chan_msg['command'] = 'join'
		Channel('chat.receive').send(chan_msg.content)


@channel_session_user
def chat_join(chan_msg):
	''' when we get a join command
	'''
	username = chan_msg.user.username
	print '%s attempting joining room %s'%(username, chan_msg['room'])
	room = Room.objects.get(title=chan_msg['room'])

	# send a signal back to the joining guy, so that they can update ther UI
	chan_msg.reply_channel.send({
		'text': json.dumps({
			'join': room.title
		})
	})

	# notify the chatroom 	 
	joinmsg = '%s joined the chatroom!'%username
	msg = Message.objects.create(
		room=room,
		message=joinmsg,
		user=username
	)
	msg.save()
	msg.send_to_group()

	# send the last 50 messages in reverse order
	for oldmsg in room.last_n_rev(50):
		print 'sending new user %s'%oldmsg
		oldmsg.send_single(chan_msg.reply_channel)

	# send the latest message last
	# msg.send_single(chan_msg.reply_channel)

	# add this person to the group! so they will be updated for future messages
	if (room.id not in chan_msg.channel_session['rooms']):
		room.ws_group.add(chan_msg.reply_channel)

	# add this room to the channel_session rooms list
	rooms = set(chan_msg.channel_session['rooms']).union([room.id])
	chan_msg.channel_session['rooms'] = list(rooms)


@channel_session_user
def chat_send(chan_msg):
	''' when we get a send command
	'''
	room = Room.objects.get(title=chan_msg['room'])
	print 'chat sent to %s'%room
	msg = Message.objects.create(
		room=room,
		message=chan_msg['message'],
		user=chan_msg.user.username
	)
	msg.save()
	msg.send_to_group()


@channel_session_user
def chat_leave(chan_msg):
	''' triggered when we get leave command
	'''
	username = chan_msg.user.username
	room = Room.objects.get(title=chan_msg['room'])
	print '%s chat leaving %s'%(username, room)

	# send message to room that user left
	leavemsg = '%s left chatroom!'%username
	msg = Message.objects.create(
		room=room,
		message=leavemsg,
		user=username
	)
	msg.save()
	msg.send_to_group()

	# send a signal back to the leaving guy, so that they can update ther UI
	chan_msg.reply_channel.send({
		'text': json.dumps({
			'leave': room.title
		})
	})

	# remove this person from the room's Group
	room.ws_group.discard(chan_msg.reply_channel)

	# remove this room from the sessions saved rooms
	rooms = set(chan_msg.channel_session['rooms']).difference([room.id])
	chan_msg.channel_session['rooms'] = list(rooms)
