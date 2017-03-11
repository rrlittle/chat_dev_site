from channels import Channel
from models import Message, Room
from channels.auth import channel_session_user
import json


def chat_create_room(chan_msg):
	''' if the room doesn't exist create it. then pass the msg onto chat_join
	'''
	try:
		Room.objects.get(title=chan_msg['room'])
	except Room.DoesNotExist:
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
	print '%s joining room %s'%(username, chan_msg['room'])
	room = Room.objects.get(title=chan_msg['room'])

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
		oldmsg.send_single(chan_msg.reply_channel)

	# send the latest message last
	msg.send_single(chan_msg.reply_channel)

	# add this person to the group! so they will be updated for future messages
	room.ws_group.add(chan_msg.reply_channel)


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
