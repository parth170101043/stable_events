from django.urls import path, include
from .views import EventApi, BtechApi, MtechApi, PhDApi, AppFeedbackApi
from rest_framework import routers


router = routers.DefaultRouter()
router.register('events', EventApi)
router.register('btech', BtechApi)
router.register('mtech', MtechApi)
router.register('phd', PhDApi)
router.register('app-feedback',AppFeedbackApi)
urlpatterns = [
    path('',include(router.urls))
]