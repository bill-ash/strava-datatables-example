import requests

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import StravaActivity, StravaToken
User = get_user_model()

# strava call back 
def callback_url(id, callbackuri): 
    """Process call back"""
    return f'http://www.strava.com/oauth/authorize?client_id={id}&response_type=code&redirect_uri={callbackuri}&approval_prompt=force&scope=activity:read'
    

def strava_auth(request):     
    """Auth"""
    callback = callback_url(
        id = settings.STRAVA_CLIENT , 
        callbackuri = 'http://0d6a-72-229-100-170.ngrok.io/stravacallback'
        )
    return redirect(callback)

def strava_callback(request): 

    resp_token = requests.post('https://www.strava.com/oauth/token', 
        data = {
            'client_id': settings.STRAVA_CLIENT, 
            'client_secret': settings.STRAVA_SECRET, 
            'code': request.GET.get('code'), 
            'grant_type': 'authorization_code'
    })

    if resp_token.status_code == 200:
        resp_token = resp_token.json()
    
    if resp_token['athlete']['username'] is None: 
        resp_token['athlete']['username'] = resp_token['athlete']['firstname']

    try:
        token = StravaToken.objects.get(user=request.user)
        token.token_type = resp_token.get('token_type'),
        token.refresh_token = resp_token.get('refresh_token')
        token.access_token = resp_token.get('access_token')
        token.strava_id = resp_token.get('athlete').get('id')
        token.strava_username = resp_token.get('athlete').get('username')
        token.save()
    except:  
        token = StravaToken(
            user=request.user,
            # token=request.GET.get('code'), 
            token_type = resp_token.get('token_type'), 
            refresh_token = resp_token.get('refresh_token'),
            access_token = resp_token.get('access_token'),
            strava_id = resp_token.get('athlete').get('id'),
            strava_username = resp_token.get('athlete').get('username')
        )
        token.save()

    return redirect('/')
    


def index(request): 
    activities = StravaActivity.objects.all()
    return render(request, 'datatables/index.html', {'activities': activities})