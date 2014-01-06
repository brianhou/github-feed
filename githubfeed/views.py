from django.http import HttpResponse
from django.shortcuts import redirect, render

def home(request):
    return render(request, 'feed/index.html')

def feed(request, username):
    if username:
        return render(request, 'feed/feed.html', {'username': username})
    return redirect('home')
