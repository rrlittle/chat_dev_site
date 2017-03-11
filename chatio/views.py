from django.shortcuts import render
import models
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required(login_url = '/admin/login/')
def index(request):
	context = {
		'rooms': models.Room.objects.all()
	}
	return render(request, 'chatio/chatexample.html', context)
