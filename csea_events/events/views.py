from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm, EventCreatorForm
from django.contrib.auth import authenticate, login, get_user_model, logout
import json
from django.http import JsonResponse
import urllib.parse
from django.contrib.auth.decorators import login_required
from .models import Event, Btech, Mtech, PhD, AppFeedback
from  django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serial import EventSerializer, BtechSerializer, MtechSerializer, PhDSerializer, AppFeedbackserializer
from datetime import date

# API viewsets for the android app
#
class EventApi(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
class BtechApi(viewsets.ModelViewSet):
    queryset = Btech.objects.all()
    serializer_class = BtechSerializer
    # permission_classes = permissions(IsAuthenticatedOrReadOnly,)

class MtechApi(viewsets.ModelViewSet):
    queryset = Mtech.objects.all()
    serializer_class = MtechSerializer
    # permission_classes = permissions(IsAuthenticatedOrReadOnly,)
class PhDApi(viewsets.ModelViewSet):
    queryset = PhD.objects.all()
    serializer_class = PhDSerializer
    # permission_classes = permissions(IsAuthenticatedOrReadOnly,)
class AppFeedbackApi(viewsets.ModelViewSet):
    queryset = AppFeedback.objects.all()
    serializer_class = AppFeedbackserializer
    


def loginPage(request):
    lform = LoginForm(request.POST or None)
    context ={'form':lform}
   
    if request.user.is_authenticated:
        return redirect('home_page')

    if lform.is_valid():
        # print(lform.cleaned_data)
        username = lform.cleaned_data.get('email')
        password = lform.cleaned_data.get('password')
        user = authenticate(request, username = username, password = password)
        
        
        if user is not None:
            login(request, user)
            
            return redirect('home_page')
        else:
            return redirect('loginPage')
            
    return render(request, 'login.html', context)



User = get_user_model()



@login_required(login_url='loginPage')
def profile_view(request):
    return render(request, 'profile.html',{'username':request.user})



# def registerPage(request):
#     rform = RegisterForm(request.POST or None)
#     context = {
#         'form':rform
#     }
#     if rform.is_valid():
#         mail = rform.cleaned_data.get('email')
#         password = rform.cleaned_data.get('password')
#         # name = rform.cleaned_data.get('name')
#         username = rform.cleaned_data.get('username')
#         # print(username)
#         add_user = User.objects.create_user(username=username, password=password)
#         user = authenticate(request, username = username, password = password)
#         if user is not None:
#             login(request, user)
#             return redirect('home_page')
#         else:
#             return render(request, 'register.html', context)
        
#         print(add_user)
#     return render(request, 'register.html', context)

def registerPage(request):

    if request.method == 'GET':
        rform = RegisterForm()
        context = {
            'form': rform
        }
        return render(request, 'register.html', context)
    else:
        rform = RegisterForm(request.POST)
        if rform.is_valid():

            department = rform.cleaned_data.get('department')
            program = rform.cleaned_data.get('program')
            roll_no = rform.cleaned_data.get('roll_no')
            phone_no = rform.cleaned_data.get('phone_no')
            print(roll_no, type(roll_no))
            email = rform.cleaned_data.get('email')
            print(email)
            password = rform.cleaned_data.get('password')
            username = rform.cleaned_data.get('name')
            add_user = User.objects.create_user(username=username, email=email, password=password)

            add_profile = Profile.objects.create(user=add_user,department=department,program=program,roll_no=str(roll_no),phone_no=str(phone_no))
            return redirect('/')
        else:
            return redirect('/register/')



@login_required(login_url='loginPage')
def create_event(request):
    form = EventCreatorForm(request.POST or None)

    if form.is_valid():
        new_event=form.save()
        new_event.requestor = str(request.user)
        new_event.save()
        print(new_event.requestor)
        form = EventCreatorForm()
    
    return render(request, 'create_event.html', {'form':form})



@login_required(login_url='loginPage')
def poll_view(request, event_id):
    events=Event.objects.filter(event_id=event_id)
    print(events[0].summary)
    context = {
        'event_name': events[0].name,
        'event_date': events[0].date,
        'event_time': events[0].time,
        'event_fee':events[0].fee,
        'contact_info':events[0].contact_info,
        'summary':events[0].summary,

    }
    return render(request,'event_info.html',context)


@login_required(login_url='loginPage')
def my_events(request):
    events_past = Event.objects.filter(requestor__exact=request.user, date__lt=date.today()).order_by('-date')
    events_today = Event.objects.filter(requestor__exact=request.user, date__exact=date.today()).order_by('-date')
    events_upcoming = Event.objects.filter(requestor__exact=request.user, date__gt=date.today()).order_by('-date')
    if events_today is None:
        busy_today='True'
    else:
        busy_today='False'
    
    return render(request, 'my-events.html', {'display_id':str(request.user), 'events_future':events_upcoming,'events_today':events_today,'events_past':events_past,'busy_today':busy_today})

@login_required(login_url='loginPage')
def home_page(request):
    events=Event.objects.filter(date__gte=date.today()).order_by('-date') 
    return render(request, 'home.html', {'display_id':str(request.user), 'events':events})


@login_required(login_url='loginPage')
def past(request):
    events=Event.objects.filter(date__lt=date.today()).order_by('-date') 
    return render(request, 'past.html', {'display_id':str(request.user), 'events':events})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('loginPage')



@login_required(login_url='loginPage')
def change_password(request):
    if request.method=='POST':
        form=PasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            logout(request)
            return redirect('loginPage')
        else:
            return redirect('change_passwd')
    else:
        form=PasswordChangeForm(user=request.user)
        args={'form':form}
        return render(request,'change_password.html',args)







@csrf_exempt
def api_resp(request):
    username = None
    password = None
    # username = request.GET.get('username')
    # password = request.GET.get('password')
    # body = json.loads(request.body)
    # content = body['content']
    # username = body['username']
    # password = body['password']
    if username is None or password is None:
        try:
            # asd = request.query_parms.get('content')
            # body_unicode = request.body.decode('utf-8')

            # data_json = urllib.parse.unquote(body_unicode)
            data_json = urllib.parse.unquote(request.body.decode('utf-8'))
            # pdb.set_trace()
            data = json.loads(data_json)
            for key in data:
                # pdb.set_trace()
                if key == 'username':
                    print(data[key])
                    username = data[key]
                elif key == 'password':
                    print(data[key])
                    password = data[key]
                else:
                    responseData = {
                        'authentication':'False',
                        'reason': 'Too many params in the request'
                    }
                    return HttpResponse(json.dumps(responseData), content_type="application/json")
        except:
            pass

    # print(data)
    # for i in data:
    #     if "username=" in i:
    #         username = i[9:]
    #         print(username)
    #     elif "password=" in i:
    #         password = i[9:]
    #         print(password)
    if username is None or password is None:
        responseData = {
            'authentication':'False',
            'reason': 'Username or Password missing in the request'
        }
        return HttpResponse(json.dumps(responseData), content_type="application/json")

    user  = authenticate(username =username,password=  password)
    print(user)
    event_list = []
    for i in Event.objects.all():
        event_list += [i.event_id]

    
    if user is not None:
        responseData = {
                'username': username,
                'password': password,
                'authenticated':'True',
                'eventList(example)' : event_list,
                'eventDates(example)' : [
                    '201904231415',
                    '201904292000'
                ]
            }
        return HttpResponse(json.dumps(responseData), content_type="application/json")
    else:
        responseData = {
            'username':username,
            'password': password,
            'authenticated':'False',
            'reason':'Password or Username is incorrect'
        }
    return HttpResponse(json.dumps(responseData), content_type="application/json")