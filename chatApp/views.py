from django.shortcuts import redirect, render
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from chatApp.models import Message
from chatApp.forms import SaveMessage
from django.db.models import Q


context = {
    'page_title' : 'Chat Room',
}

# Create your views here.
def login(request):
    if request.method == 'POST':
        request.session['logged_user'] = request.POST['username']
        message = Message(username = request.POST['username'],msg_type = 1).save()
        request.session['logged_id'] = Message.objects.all().last().id
        return redirect('home-page')
    else:
        context['id'] = ''
        if 'logged_id' in request.session:
            context['id'] = request.session['logged_id']
            del request.session['logged_id']
        return render(request, 'login.html', context)

def home(request):
    if 'logged_user' in request.session:
        context['page_title'] = 'Logged In | Chat Room'
        context['chats'] = Message.objects.all().order_by('-date_added')[:10]
        context['id'] = ''
        if 'logged_id' in request.session:
            context['id'] = request.session['logged_id']
            del request.session['logged_id']

        return render(request,'home.html', context)
    else:
        return redirect('login-page')
def logout(request):
    if 'logged_user' in request.session:
        message = Message(username = request.session['logged_user'],msg_type = 2).save()
        del request.session['logged_user']
        request.session['logged_id'] = Message.objects.all().last().id
    return redirect('login-page')

def send_message(request):
    resp = {'status':'failed','msg':''}
    if request.method == 'POST':
        form = SaveMessage(request.POST)
        if form.is_valid():
            form.save()
            resp['status'] = 'success'
            resp['id'] = Message.objects.all().last().id
        else:
            resp['msg'] = "Sending Message Failed"
            for field in form:
                for error in field.errors:
                    resp['msg'] += str("<br>" + error)
    return HttpResponse(json.dumps(resp),content_type="application/json")

def load_more(request,pk=None):
    resp = {'status':'failed','data':''}
    data = []
    if not pk is None:
        chats = Message.objects.filter(id__lt =  pk).all().order_by('-id')[:10]
        for chat in  chats:
            data.append({'id':chat.id,'message':chat.get_message(),'username':chat.username})
        resp['data'] = data
        resp['status'] = 'success'
    return HttpResponse(json.dumps(resp),content_type="application/json")

