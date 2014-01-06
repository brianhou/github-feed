from django.http import HttpResponse
from django.shortcuts import redirect

def home(request):
    return HttpResponse('githubfeed: go to /feed/your-username')

def feed(request, username):
    if username:
        return HttpResponse('you are at /feed/{}'.format(username))
    return redirect('home')
