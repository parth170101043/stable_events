from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


from django.contrib.auth.models import User
department_values = (
        ('cse', 'Computer Science & Engineering'),
        ('ece', 'Electronics & Communication Engineering'),
        ('me', 'Mechanical Engineering'),
        ('ce', 'Civil Engineering'),
        ('dd', 'Design'),
        ('bsbe', 'Biosciences & Bioengineering'),
        ('cl', 'Chemical Engineering'),
        ('cst', 'Chemical Science & Technology'),
        ('eee', 'Electronics & Electrical Engineering'),
        ('ma', 'Mathematics & Computing'),
        ('ph', 'Engineering Physics'),
        ('rt', 'Rural Technology'),
        ('hss', 'Humanities & Social Sciences'),
        ('enc', 'Centre for Energy'),
        ('env', 'Centre for Environment'),
        ('nt', 'Centre for Nanotechnology'),
        ('lst', 'Centre for Linguistic Science & Technology')
    )
program_values = (
        ('btech', 'BTech'),
        ('mtech', 'MTech'),
        ('phd', 'PhD'),
        ('msc', 'MSc'),
        ('msr', 'MS-R'),
        ('ma', 'MA'),
        ('bdes', 'BDes'),
        ('mdes', 'MDes')
    )
# Create your models here.
class Btech(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Mtech(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PhD(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Event(models.Model):

    # todo, extend and test by sunday

    name = models.CharField(max_length=300)
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular event')
    fee = models.PositiveIntegerField()
    capacity  = models.PositiveIntegerField()
    target_audience = models.CharField(max_length=300)
    date = models.DateField(null = False, blank = False)
    time = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    faq = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=300, help_text=' (Press Ctrl to select multiple)')
    organisors = models.CharField(max_length=300)
    contact_info = models.CharField(max_length=300)
    venue = models.CharField(max_length=50, choices=(('L1','Lecture Hall 1'),('L2','Lecture Hall 2'),('L1','Lecture Hall 3'),('L1','Lecture Hall 4'),('Audi','Auditorium')),default='Audi')
    # requester = models.ForeignKey(User, unique=True, on_delete=models.CASCADE, default=None)
    invitees_btech = models.ManyToManyField(Btech, help_text=' (Press Ctrl to select multiple)', blank=True)
    invitees_mtech = models.ManyToManyField(Mtech, help_text=' (Press Ctrl to select multiple)', blank=True)
    invitees_phd = models.ManyToManyField(PhD, blank=True)
    # invitees_btech = models.ManyToManyField(Btech, help_text=' (Press Ctrl to select multiple)')
    comment_for_admin = models.CharField(max_length=300)
    approval = models.CharField(max_length=50, choices = (('Appr','Approved'),('Pend','Pending'),('Decl','Declined')), default='Pend')
    requestor = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Poll(models.Model):

    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    response_coming = models.PositiveIntegerField()
    response_not_coming  = models.PositiveIntegerField()
    response_not_sure = models.PositiveIntegerField()

class Profile(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    department = models.CharField(max_length=100,blank=False,choices=department_values)
    program = models.CharField(max_length=100,blank=False,choices=program_values)
    roll_no = models.BigIntegerField(unique=True,blank=False)
    phone_no = models.BigIntegerField(blank=False)

class AppFeedback(models.Model):

    content = models.TextField(blank=False)