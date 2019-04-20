from rest_framework import serializers
from .models import Event, Btech, Mtech, PhD, AppFeedback, EventFeedback, Profile
from django.contrib.auth import get_user_model
#
#
#The serializer module for the API
#
#
#Function to display the events in an order 
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('url','requestor','event_id','name','fee','capacity','date','time','venue','tags','invitees_btech','invitees_mtech','invitees_phd','organisors','contact_info','summary','faq','image_string','comment_for_admin','curr_audience','approval')
#Function to display the Btech programs based on the year 
class BtechSerializer(serializers.ModelSerializer):
    class Meta:
        model = Btech
        fields = ('id','url','name',)
        
#Function to display the Mtech programs based on the year 
class MtechSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mtech
        fields = ('id','url','name',)
        
#Function to display the PhD programs based on the year 
class PhDSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhD
        fields = ('id','url','name',)
        #Function to display the feedbacks given by the users in an order 
class AppFeedbackserializer(serializers.ModelSerializer):
    class Meta:
        model = AppFeedback
        fields = ('id','url','content','rating_ui','rating_ux','rating_overall','submitted_by')

class EventFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventFeedback
        fields = ('id','url','content','submiter','rating','to_event')
#Function to display the Profile of the user
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id','url','user','department','program','roll_no','phone_no')
