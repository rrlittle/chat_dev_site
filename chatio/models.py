from __future__ import unicode_literals

from django.db import models
from channels import Group
from django.utils import timezone
import json


# Create your models here.
class Room(models.Model):
	title = models.CharField(max_length=255)

	@property
	def ws_group(self):
		return Group('chatroom-%s'%self.id)

	def __str__(self):
		return self.title

	def last_n(self, n):
		''' return the latest n messages mostrecent - oldest'''
		return list(Message.objects.filter(room=self).order_by('created'))[-n:]


class Message(models.Model):
	user = models.CharField(max_length=20)
	message = models.CharField(max_length=500)
	room = models.ForeignKey(Room)
	created = models.DateTimeField(default=timezone.now)

	def send_to_group(self):
		msg = {
			'room': str(self.room),
			'message': self.message,
			'created': str(self.created),
			'username': self.user
		}
		self.room.ws_group.send({
			'text': json.dumps(msg)
		}, immediately=True)

	def send_single(self, reply_channel):
		msg = {
			'room': str(self.room),
			'message': self.message,
			'created': str(self.created),
			'username': self.user
		}
		reply_channel.send({
			'text': json.dumps(msg)
		}, immediately=True)

	def __str__(self):
		return '[%s]%s:%s'%(str(self.room), self.user, self.message)
