from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm, EventCreatorForm, FeedbackForm, PollCreatorForm
from django.contrib.auth import authenticate, login, get_user_model, logout
import json
from django.http import JsonResponse
import urllib.parse
from django.contrib.auth.decorators import login_required
from .models import Event, Btech, Mtech, PhD, AppFeedback, Profile, EventFeedback, Poll, Vote
from  django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serial import EventSerializer, BtechSerializer, MtechSerializer, PhDSerializer, AppFeedbackserializer, EventFeedbackSerializer, ProfileSerializer
from datetime import date
from django.contrib.auth import update_session_auth_hash
# API viewsets for the android app
#




class ProfileApi(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
class EventApi(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-date')
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

class EventFeedbackApi(viewsets.ModelViewSet):
    queryset = EventFeedback.objects.all()
    serializer_class = EventFeedbackSerializer
# todo
# make the api faq and the web faq sync
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
def feedback_view(request, id):
    if request.method == 'GET':
        eve = Event.objects.filter(event_id__exact=id)
        feeds = EventFeedback.objects.filter(to_event=eve[0],submiter__exact=str(request.user))
        try:
            form = FeedbackForm(initial={'rating':feeds[0].rating,'content':feeds[0].content})
        except:
            form = FeedbackForm()
        return render(request,'feedback.html',{'form':form})
    else:
        form = FeedbackForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get('content')
            rating = form.cleaned_data.get('rating')
            concerned_event = Event.objects.filter(event_id__exact=id)
            search = EventFeedback.objects.filter(to_event__exact=concerned_event[0],submiter__exact=str(request.user))
            
            
            try:
                search[0].delete()
                feed= EventFeedback.objects.create(content=content,submiter=str(request.user),rating=rating,to_event=concerned_event[0])
                feed.save()
            except:
                feed= EventFeedback.objects.create(content=content,submiter=str(request.user),rating=rating,to_event=concerned_event[0])
                feed.save()
            
            return redirect('past')
            # return render(request,'feedback.html',{'form':form})
        return render(request,'feedback.html',{'form':form})




@login_required(login_url='loginPage')
def profile_view(request):
    try:
        prof = Profile.objects.filter(user=request.user)[0]
        return render(request, 'profile.html',{'username':request.user,'email':request.user.email,'first_name':request.user.first_name,'last_name':request.user.last_name,'phone_no':prof.phone_no,'roll_no':prof.roll_no,'dept':prof.roll_no,'dept':prof.department,'course':prof.program,})
    except:
        return render(request, 'profile.html',{'username':request.user,'email':request.user.email,'first_name':request.user.first_name,'last_name':request.user.last_name,})
  
    



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
            # print(roll_no, type(roll_no))
            email = rform.cleaned_data.get('email')
            print(email)
            mail_stuff = email.split('@')
            first_name=rform.cleaned_data.get('first_name')
            last_name=rform.cleaned_data.get('last_name')
            password = rform.cleaned_data.get('password')
            username = mail_stuff[0]
            # username = rform.cleaned_data.get('name')
            add_user = User.objects.create_user(username=username, email=email, password=password)
            add_user.first_name = first_name
            add_user.last_name = last_name
            add_user.save()
            # print(username)
            add_profile = Profile.objects.create(user=add_user,department=department,program=program,roll_no=str(roll_no),phone_no=str(phone_no))
            return redirect('/register/')
        else:
            return render(request, 'register.html', {'form':rform})


def api_change_pw(request):

    username = None
    old_password = None
    new_password = None
    try:
        data_json = urllib.parse.unquote(request.body.decode('utf-8'))
        # pdb.set_trace()
        data = json.loads(data_json)
        for key in data:
            # pdb.set_trace()
            if key == 'username':
                print(data[key])
                username = data[key]
            elif key == 'old_password':
                print(data[key])
                password = data[key]
            elif key == 'new_password':
                print(data[key])
                password = data[key]
            else:
                responseData = {
                    'error_code':1
                }
                return HttpResponse(json.dumps(responseData), content_type="application/json")
    except:
        pass

    user = authenticate(username= username,password=old_password)

    if user is None:
        return HttpResponse(json.dumps({'error':'wrong username or password'}), content_type="application/json")

    else:
        user.set_password(new_password)
        return HttpResponse(json.dumps({'response':'password successfully changed'}), content_type="application/json")


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
        'faq':events[0].faq

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
    events=Event.objects.filter(date__gte=date.today()).order_by('date') 
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



def event_edit(request, id): 
    instance = get_object_or_404(Event, event_id=id)
    form = EventCreatorForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('my_events')
    return render(request, 'create_event.html', {'form':form})




@csrf_exempt
def api_resp(request):
    username = None
    password = None
    try:
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
                    'error_code':1
                }
                return HttpResponse(json.dumps(responseData), content_type="application/json")
    except:
        pass
    if username is None or password is None:
        responseData = {
            'error_code':2
        }
        return HttpResponse(json.dumps(responseData), content_type="application/json")
 
    user  = authenticate(username =username,password=  password)
    print(user)
    # q = User.objects.filter(username=username)
    p = Profile.objects.filter(user = user)
    if p.count() == 0:
        return HttpResponse(json.dumps({'error':'user+password combination wrong'}), content_type="application/json")
    p=p[0]
    if user is not None:
        responseData = {
        'error_code':0 ,
        'username':username,
        # 'name':q.first_name + " " + q.last_name,
        'roll':p.roll_no,
        'branch': p.department,
        'year':'20'+str(p.roll_no)[0:2],
        'stream':p.program,
        'phone':p.phone_no
        }
        return HttpResponse(json.dumps(responseData), content_type="application/json")
    else:
        responseData = {
            'error_code':3
        }
    return HttpResponse(json.dumps(responseData), content_type="application/json")
 
    username = None
    password = None
    
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
        except:
            responseData={
            'response':'error: username or password missing',
            'expected-structure':{
                'username':'<username>',
                'password':'<password>'
                }
            }
            return HttpResponse(json.dumps(responseData), content_type="application/json")

        user = authenticate(username = username, password = password)
        if user is not None:
            responseData={
                'response':'successfully logged in',
                'logged-in-as':username
            }
            return HttpResponse(json.dumps(responseData), content_type="application/json")
        else:
            responseData={
                'response':'unable to log-in',
                'reason':'username or password wrong'
            }
            return HttpResponse(json.dumps(responseData), content_type="application/json")


        
    else:
        responseData={
            'response':'error: send a proper request of type- POST',
            'expected-structure':{
                'username':'<username>',
                'password':'<password>'
            }
        }
        return HttpResponse(json.dumps(responseData), content_type="application/json")



@csrf_exempt
def api_reg(request):
    args={
            "error":"send a request as following ",
            "structure":{
                "first_name":'<name>',
                "last_name":'<name>',
                'email':'<mail>@iitg.ac.in',
                'password':"<password>",
                'dept':'<cse/ece/me/ce/dd/bsbe/cl/cst/eee/ma/ph/rt/hss/enc/env/nt/lst>',
                'prog':'<btech/mtech/phd/msc/msr/ma/bdes/mdes>',
                'roll_no':'<roll>',
                'phone_no':'<phone>'
            }
        }
    
    try:
        data_json = urllib.parse.unquote(request.body.decode('utf-8'))
        # pdb.set_trace()
        data = json.loads(data_json)
        for key in data:
            # pdb.set_trace()
            if key == 'email':
                print(data[key])
                email = data[key]
            elif key == 'password':
                print(data[key])
                password = data[key]
            elif key == 'first_name':
                print(data[key])
                first_name = data[key]
            elif key == 'last_name':
                print(data[key])
                last_name = data[key]
            elif key == 'dept':
                print(data[key])
                dept = data[key]
            elif key == 'prog':
                print(data[key])
                prog=data[key]
            elif key == 'roll_no':
                print(data[key])
                roll_no = data[key]
            elif key == 'phone_no':
                print(data[key])
                phone_no = data[key]
            else:
                responseData = {
                    'error_code':1,
                    'info':'all keys not found, send a request as follows',
                    'expected-data':{
                    "first_name":'<name>',
                    "last_name":'<name>',
                    'email':'<mail>@iitg.ac.in',
                    'password':"<password>",
                    'dept':'<cse/ece/me/ce/dd/bsbe/cl/cst/eee/ma/ph/rt/hss/enc/env/nt/lst>',
                    'prog':'<btech/mtech/phd/msc/msr/ma/bdes/mdes>',
                    'roll_no':'<roll>',
                    'phone_no':'<phone>'
                }

                }
                return HttpResponse(json.dumps(responseData), content_type="application/json")

    except:

        return HttpResponse(json.dumps(args), content_type="application/json")
    

    if not first_name or not last_name:
        return HttpResponse(json.dumps({'error':"first and last name can't be empty"}), content_type="application/json")
    if not 'iitg.ac.in' in email:
        return HttpResponse(json.dumps({'error':"use iitg mail only"}), content_type="application/json")
    if not password:
        return HttpResponse(json.dumps({'error':"password can't be empty"}), content_type="application/json")
    if not roll_no or not phone_no or not dept or not prog:
        return HttpResponse(json.dumps({'error':"some field(s) is/are empty"}), content_type="application/json")

    queryset = User.objects.filter(email=email)
    if queryset.exists():
        return HttpResponse(json.dumps({'error':"email already active"}), content_type="application/json")
    username = email.split('@')[0]

    test = Profile.objects.filter(roll_no__exact=roll_no)
    if test.count() != 0:
        return HttpResponse(json.dumps({'error':1,'reason':'roll_no already active'}), content_type="application/json")

    add_user = User.objects.create_user(username=username, email=email, password=password)
    add_user.first_name = first_name
    add_user.last_name = last_name
    add_user.save()
    # print(username)
    add_profile = Profile.objects.create(user=add_user,department=dept,program=prog,roll_no=str(roll_no),phone_no=str(phone_no))
    return HttpResponse(json.dumps({'registration status':"success",'your-username':username}), content_type="application/json")

    
    return HttpResponse(json.dumps({'error':'unknown server error, check back-end code '}), content_type="application/json")




@login_required(login_url='loginPage')
def poll_count_view(request,event_id):
    poll= Event.objects.filter(event_id=event_id)
    temp=Poll.objects.filter(event_id=event_id)
    if not temp:
        temp = Poll(event_id=event_id,response_coming=0,response_not_coming=0,response_not_sure=0)
        response_coming=temp.response_coming
        response_not_coming=temp.response_not_coming
        response_not_sure=temp.response_not_sure
        id_event=temp.event_id
        temp.save()
    else:
            response_coming=temp[0].response_coming
            response_not_coming=temp[0].response_not_coming
            response_not_sure=temp[0].response_not_sure
            id_event=temp[0].event_id   
       # print(temp.event_id)
    context = {
        'response_coming' : response_coming,
        'response_not_coming' : response_not_coming,
        'response_not_sure' : response_not_sure ,
        'kk':id_event,

    }  
    #temp.save()    
    return render(request,'poll_view.html',context)

@login_required(login_url='loginPage')
def poll_vote(request,event_id):   
    poll=Poll.objects.get(event_id=event_id)
    id_user=str(request.user)
    temp1=Poll.objects.filter(event_id=event_id)
    flag=0
    temp_str=str(temp1[0].user_id)
    if (temp_str.find(id_user)!=-1):
        flag=1
    else :
        pass    

    if (flag==0):
        poll.user_id=poll.user_id + id_user + ', '
        vote=Vote(vote_id=event_id,user_id=id_user,user_vote=4)
        form = PollCreatorForm(data=request.POST)

        if(request.method=='POST'):
            if form.is_valid():
                data_temp=form.save(event_id,poll,request)
                #poll.save()
                if (data_temp=='response_not_coming'):
                    vote.user_vote=1
                elif (data_temp=='response_coming'):
                    vote.user_vote=2
                else:
                    vote.user_vote=3      
                vote.save()      
                form = PollCreatorForm()
                return redirect('poll_count',event_id)
            else :
                return redirect('poll_count_vote', event_id)
    else :
        context ={
            'kk':event_id,
            'everything':id_user
        }
        return render(request,'done.html',context=context)        
    return render(request, 'poll_vote.html', {'form':form})

@login_required(login_url='loginPage')
def poll_modify(request,event_id):
    id_user=request.user
    vote=Vote.objects.filter(vote_id=event_id,user_id=id_user)

    if vote:
        poll=Poll.objects.filter(event_id=event_id)
        # temp_data=vote[0].user_vote
        
        # if (temp_data==1):
        #     poll[0].response_not_coming=poll[0].response_not_coming -1
        # elif (temp_data==2):
        #     poll[0].response_coming=poll[0].response_coming - 1
        # else :
        #     poll[0].response_not_sure=poll[0].response_not_sure -1 
        # poll[0].save()
        form = PollCreatorForm(data=request.POST)

        if(request.method=='POST'):
            if form.is_valid():
                data_temp=form.save(event_id,poll[0],request)
                #poll.save()
                if (data_temp=='response_not_coming'):
                    vote[0].user_vote=1
                elif (data_temp=='response_coming'):
                    vote[0].user_vote=2
                else:
                    vote[0].user_vote=3      
                vote[0].save()      
                form = PollCreatorForm()
                return redirect('poll_count',event_id)
            else :
                return redirect('poll_count_vote', event_id)
    else :
        context = {
            'kk' : event_id,
        }
        return render(request,'error.html',context)  

    return render(request, 'poll_vote.html', {'form':form})
  
    