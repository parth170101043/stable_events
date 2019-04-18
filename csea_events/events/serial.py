from rest_framework import serializers
from .models import Event, Btech, Mtech, PhD, AppFeedback
#
#
#The serializer module for the API
#
#

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('url','name','fee','capacity','target_audience','date','time','venue','tags','invitees_btech','invitees_mtech','invitees_phd','organisors','contact_info','summary','faq','comment_for_admin')

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