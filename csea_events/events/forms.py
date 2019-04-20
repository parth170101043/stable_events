from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from . import models
from .models import Event, Poll, Vote
from django.forms import formset_factory, modelformset_factory


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Your @iitg email'
            }), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Your password'}), required=True)

class FeedbackForm(forms.Form):
    content = forms.CharField( widget=forms.Textarea )
    rating = forms.IntegerField(max_value=10, min_value=0)

User = get_user_model()


# class RegisterForm(forms.Form):
#     name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your Full Name'}),required=True)
#     email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your college email (@iitg.ac.in)'}), required=True)
#     username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'select a username' }), required=True)
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Your password'}), required=True)
#     confirm_password = forms.CharField( label = 'Confirm Password', widget=forms.PasswordInput(attrs={'placeholder':'Your password (again)'}), required=True)


#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         queryset = User.objects.filter(username = email)

#         if 'iitg.ac.in' not in email:
#             raise forms.ValidationError("Enter a valid email")
#         if queryset.exists():
#             raise forms.ValidationError("Email already active")
#         return email



#     def clean_confirm_password(self):
#         passw = self.cleaned_data.get('confirm_password')
#         passw_orig = self.cleaned_data.get('password')

#         if passw != passw_orig:
#             raise forms.ValidationError('Both passwords must match')
        
#         return passw


class EventCreatorForm(ModelForm):
    class Meta:
        model = models.Event
        fields =['name','fee','capacity','target_audience','date','time','venue','tags','invitees_btech','invitees_mtech','invitees_phd','organisors','contact_info','summary','comment_for_admin','faq_question_1','faq_answer_1','faq_question_2','faq_answer_2']


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

class RegisterForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your First Name'}),
                           required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Last Name'}),
                           required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your @iitg email'
    }), required=True)
    department = forms.CharField(widget=forms.Select(choices=department_values,attrs={'class': 'form-control'}),required=True)
    program = forms.CharField(widget=forms.Select(choices=program_values, attrs={'class': 'form-control'}),
                                 required=True)
    roll_no = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Your Roll Number'}),
                           required=True)
    phone_no = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone Number'}),
                           required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Your password'}), required=True)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Your password (again)'}), required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        print(1,email)
        queryset = User.objects.filter(email=email)

        if queryset.exists():
            print(1)
            raise forms.ValidationError("Email already active")
        return email

    def clean_confirm_password(self):
        passw = self.cleaned_data.get('confirm_password')
        passw_orig = self.cleaned_data.get('password')

        if passw != passw_orig:
            raise forms.ValidationError('Both passwords must match')

        return passw


class PollCreatorForm(forms.Form):
    choices=[
        ('response_not_coming','Not Coming'),
        ('response_coming','Coming'),
        ('response_not_sure','Not Sure'),
    ]
    f_value=forms.ChoiceField(choices=choices)

    def save(self,event_id,poll,request):
        vote=Vote.objects.filter(vote_id=event_id,user_id=str(request.user))
        cleaned_data=self.cleaned_data.get('f_value')
        if vote:
            temp_data=vote[0].user_vote
        
            if (temp_data==1):
                poll.response_not_coming=poll.response_not_coming -1
            elif (temp_data==2):
                poll.response_coming=poll.response_coming - 1
            else :
                poll.response_not_sure=poll.response_not_sure -1 
        else :
            pass   
            
        if (cleaned_data=='response_not_coming'):
            poll.response_not_coming=poll.response_not_coming + 1 
        elif (cleaned_data=='response_coming'):
            poll.response_coming = poll.response_coming + 1
        else:
            poll.response_not_sure= poll.response_not_sure + 1
        poll.save()
        return cleaned_data

