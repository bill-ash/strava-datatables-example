import requests 
from datatables.models import StravaToken, StravaActivity
StravaActivity.objects.all()
token = StravaToken.objects.first()
token.get_miles().json()
# token.get_activities().json()
token.sync_activities()
