from django.contrib import admin
from events.models import Event, Btech, Mtech, PhD, AppFeedback, Profile, EventFeedback
# Register your models here.
#Each model maps to a single database table and each attribute of the model represents a database field.
class EventAdmin(admin.ModelAdmin):  
  list_display = ('approval','venue','date','time','requestor','name')
  ordering = ('approval',) # The negative sign indicate descendent order
class ProfileAdmin(admin.ModelAdmin):  
  list_display = ('roll_no','user','department','phone_no')
  ordering = ('roll_no',) # The negative sign indicate descendent order
admin.site.register(EventFeedback)

admin.site.register(Event, EventAdmin)

admin.site.register(Btech)

admin.site.register(Mtech)

admin.site.register(PhD)

admin.site.register(AppFeedback)

admin.site.register(Profile,ProfileAdmin)