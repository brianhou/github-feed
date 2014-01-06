from django.http import HttpResponse
from django.shortcuts import redirect, render
from githubfeed.feed import recent_commits, limit

def home(request):
    return render(request, 'feed/index.html')

def feed(request, username):
    if username:
        data = {
            'username' : username,
            'recent_commits' : recent_commits(username)
            }
        return render(request, 'feed/feed.html', data)
    return redirect('home')

def rate(request):
    remaining, max = limit()
    return HttpResponse('{}/{} requests remaining'.format(remaining, max))
