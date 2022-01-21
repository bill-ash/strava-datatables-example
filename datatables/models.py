import requests
from django.db import models
from django.conf import settings 
from django.contrib.auth import get_user_model
from django.db import models

class Basetable(models.Model):
	basetable_id = models.AutoField(primary_key=True)
	comment_count = models.CharField(max_length=100)
	has_kudoed = models.BooleanField()
	device_watts = models.BooleanField()
	type = models.CharField(max_length=100)
	end_latlng = models.CharField(max_length=100)
	upload_id_str = models.CharField(max_length=100)
	id = models.CharField(max_length=100)
	kudos_count = models.CharField(max_length=100)
	kilojoules = models.CharField(max_length=100)
	visibility = models.CharField(max_length=100)
	athlete_count = models.CharField(max_length=100)
	resource_state = models.CharField(max_length=100)
	max_speed = models.CharField(max_length=100)
	from_accepted_tag = models.BooleanField()
	start_latlng = models.CharField(max_length=100)
	achievement_count = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	commute = models.BooleanField()
	utc_offset = models.CharField(max_length=100)
	average_cadence = models.CharField(max_length=100)
	private = models.BooleanField()
	upload_id = models.CharField(max_length=100)
	distance = models.CharField(max_length=100)
	timezone = models.CharField(max_length=100)
	location_country = models.CharField(max_length=100)
	has_heartrate = models.BooleanField()
	external_id = models.CharField(max_length=100)
	location_state = models.CharField(max_length=100)
	manual = models.BooleanField()
	gear_id = models.CharField(max_length=100)
	flagged = models.BooleanField()
	trainer = models.BooleanField()
	start_latitude = models.CharField(max_length=100)
	workout_type = models.CharField(max_length=100)
	location_city = models.CharField(max_length=100)
	total_photo_count = models.CharField(max_length=100)
	elapsed_time = models.IntegerField()
	heartrate_opt_out = models.BooleanField()
	display_hide_heartrate_option = models.BooleanField()
	average_speed = models.CharField(max_length=100)
	average_temp = models.IntegerField()
	moving_time = models.IntegerField()
	start_date = models.CharField(max_length=100)
	pr_count = models.CharField(max_length=100)
	start_date_local = models.CharField(max_length=100)
	total_elevation_gain = models.CharField(max_length=100)
	average_watts = models.CharField(max_length=100)
	start_longitude = models.CharField(max_length=100)
	photo_count = models.CharField(max_length=100)
	max_watts = models.IntegerField()
	weighted_average_watts = models.IntegerField()
	
class Athlete(models.Model):
	basetable_id = models.OneToOneField(Basetable,on_delete=models.CASCADE)
	athlete_id = models.AutoField(primary_key=True)
	resource_state = models.CharField(max_length=100)
	id = models.IntegerField()
	
class Map(models.Model):
	basetable_id = models.OneToOneField(Basetable,on_delete=models.CASCADE)
	map_id = models.AutoField(primary_key=True)
	summary_polyline = models.CharField(max_length=100)
	id = models.CharField(max_length=100)
	resource_state = models.CharField(max_length=100)
	

class StravaActivity(models.Model): 
    name = models.CharField(max_length=200, null=True, blank=True)
    distance = models.CharField(max_length=200, null=True, blank=True)
    moving_time = models.CharField(max_length=200, null=True, blank=True)
    elapsed_time = models.CharField(max_length=200, null=True, blank=True)
    total_elevation_gain = models.CharField(max_length=200, null=True, blank=True)
    workout_type = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.CharField(max_length=200, null=True, blank=True)
    location_city = models.CharField(max_length=200, null=True, blank=True)
    location_state = models.CharField(max_length=200, null=True, blank=True)
    location_country = models.CharField(max_length=200, null=True, blank=True)
    achievement_count = models.CharField(max_length=200, null=True, blank=True)
    kudos_count = models.CharField(max_length=200, null=True, blank=True)
    comment_count = models.CharField(max_length=200, null=True, blank=True)
    photo_count = models.CharField(max_length=200, null=True, blank=True)
    average_speed = models.CharField(max_length=200, null=True, blank=True)
    max_speed = models.CharField(max_length=200, null=True, blank=True)
    average_temp = models.CharField(max_length=200, null=True, blank=True)
    average_watts = models.CharField(max_length=200, null=True, blank=True)
    pr_count = models.CharField(max_length=200, null=True, blank=True)
    has_kudoed = models.CharField(max_length=200, null=True, blank=True)

class StravaToken(models.Model): 
    user = models.OneToOneField(
        get_user_model(), 
        on_delete=models.CASCADE
    )
    token_type = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=1200)
    access_token = models.CharField(max_length=1200)
    strava_id = models.CharField(max_length=200)
    strava_username = models.CharField(max_length=200)

    def __str__(self): 
        return self.user.username

    def get_activities(self): 
        auth_header = {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + self.access_token,
        }
        url = 'https://www.strava.com/api/v3/athlete/activities?per_page=100'

        return requests.get(url, headers=auth_header).json()

    def get_miles(self): 
        auth_header = {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + self.access_token,
        }
        url = f"https://www.strava.com/api/v3/athletes/{self.strava_id}/stats"

        return requests.get(url, headers=auth_header)

    def sync_activities(self): 
        activities = self.get_activities()
        for strava in activities: 
            activity = StravaActivity()
            activity.name = strava.get('name', '')
            activity.distance = strava.get('distance', '')
            activity.moving_time = strava.get('moving_time', '')
            activity.elapsed_time = strava.get('elapsed_time', '')
            activity.total_elevation_gain = strava.get('total_elevation_gain', '')
            activity.workout_type = strava.get('workout_type', '')
            activity.start_date = strava.get('start_date', '')
            activity.location_city = strava.get('location_city', '')
            activity.location_state = strava.get('location_state', '')
            activity.location_country = strava.get('location_country', '')
            activity.achievement_count = strava.get('achievement_count', '')
            activity.kudos_count = strava.get('kudos_count', '')
            activity.comment_count = strava.get('comment_count', '')
            activity.photo_count = strava.get('photo_count', '')
            activity.average_speed = strava.get('average_speed', '')
            activity.max_speed = strava.get('max_speed', '')
            activity.average_temp = strava.get('average_temp', '')
            activity.average_watts = strava.get('average_watts', '')
            activity.pr_count = strava.get('pr_count', '')
            activity.has_kudoed = strava.get('has_kudoed', '')
            activity.save()





    


