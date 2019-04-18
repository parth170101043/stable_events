from django.urls import path, include
from .views import EventApi, BtechApi, MtechApi, PhDApi, AppFeedbackApi, EventFeedbackApi, ProfileApi
from rest_framework import routers


router = routers.DefaultRouter()
router.register('events', EventApi)
router.register('btech', BtechApi)
router.register('mtech', MtechApi)
router.register('phd', PhDApi)
router.register('app-feedback',AppFeedbackApi)
router.register('event-feedback',EventFeedbackApi)
router.register('profile',ProfileApi)
urlpatterns = [
    path('',include(router.urls))
]