from rest_framework import serializers
from .models import Event, Btech, Mtech, PhD, AppFeedback, EventFeedback, Profile
from django.contrib.auth import get_user_model
#
#
#The serializer module for the API
#
#

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('url','event_id','name','fee','capacity','target_audience','date','time','venue','tags','invitees_btech','invitees_mtech','invitees_phd','organisors','contact_info','summary','faq','image_string','comment_for_admin','curr_audience','approval')

class BtechSerializer(serializers.ModelSerializer):
    class Meta:
        model = Btech
        fields = ('id','url','name',)
        

class MtechSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mtech
        fields = ('id','url','name',)
        

class PhDSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhD
        fields = ('id','url','name',)
        
class AppFeedbackserializer(serializers.ModelSerializer):
    class Meta:
        model = AppFeedback
        fields = ('id','url','content')

class EventFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventFeedback
        fields = ('id','url','content','submiter','rating','to_event')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id','url','user','department','program','roll_no','phone_no')
