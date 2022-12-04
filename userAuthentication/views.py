from django.shortcuts import render
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from .forms import signInForm, signUpForm
from .models import user
import json
from meetingMinutes import settings
#Html Mails
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.core.mail import EmailMessage
from userAuthentication.tokken import account_activation_token
from django.views.generic.base import TemplateView

# Create your views here.

class UserSignIN(View):
    def get(self,request):
        form=signInForm()
        return render(request,"userAuthentication/signIn.html",{"form":form})
    
    def post(self,request):
        form=signInForm(request.POST)
        if(form.is_valid()):
            userEmail=form.cleaned_data["userEmail"]
            userPassword=form.cleaned_data["userPassword"]
            print("AK")
            print(userEmail)
            try:
                myUser=user.objects.get(userEmail=userEmail,userPassword=userPassword)
                if(myUser.activationStatus):
                    request.session["userEmail"] = form.cleaned_data["userEmail"]
                    return HttpResponse(json.dumps({'message': 0}))
                else:
                    return HttpResponse(json.dumps({'message': -3}))
            except:
                return HttpResponse(json.dumps({'message': -2}))
        else:
            json_dump = json.loads(form.errors.as_json())
            key=list(json_dump.keys())[0]
            errorMessage=json_dump[key][0]['message']
            return HttpResponse(json.dumps({'message': -1,'error':errorMessage}))

class UserSignUp(View):
    def get(self,request):
        form=signUpForm()
        return render(request,"userAuthentication/signUp.html",{"form":form})
    def post(self,request):
        form=signUpForm(request.POST)
        if(form.is_valid()):
            if(form.cleaned_data["userPassword"]==form.cleaned_data["confirmPassword"]):
                newUser=user(firstName=form.cleaned_data["firstName"],lastName=form.cleaned_data["lastName"],userEmail=form.cleaned_data["userEmail"],userPassword=form.cleaned_data["userPassword"])
                try:
                    #Saving User To DB
                    self.__addUser(newUser,form)
                    #Sending verification Email
                    current_site = get_current_site(request)
                    self.__mailUserForAuthenticaton(current_site,newUser)
                    return HttpResponse(json.dumps({'message': 0,'email':newUser.userEmail}))
                except:
                    return HttpResponse(json.dumps({'message': -3}))
            else:
                return HttpResponse(json.dumps({'message': -2}))
        else:
            json_dump = json.loads(form.errors.as_json())
            key=list(json_dump.keys())[0]
            errorMessage=json_dump[key][0]['message']
            return HttpResponse(json.dumps({'message': -1,'error':errorMessage}))
        
    def __addUser(self,newUser,form):
        if(form.cleaned_data["contactNumber"]!=""):
            newUser.contactNumber=form.cleaned_data["contactNumber"]
        if(form.cleaned_data["organizationName"]!=""):
            newUser.organizationName=form.cleaned_data["organizationName"]
        myUsers=user.objects.all()
        if(len(myUsers)>0):
            newUser.userID=(myUsers[len(myUsers)-1].userID)+1
        newUser.save(force_insert=True)
        
    def __mailUserForAuthenticaton(self,currentSite,user):
        mail_subject = 'Meeting Minutes Account Activation'  
        htmlContent = render_to_string('userAuthentication/activateAccount.html', {  
            'userEmail': user.userEmail,  
            'domain': currentSite.domain,  
            'uid':urlsafe_base64_encode(force_bytes(user.userEmail)),  
            'token':account_activation_token.make_token(user),  
        })
        text_content=strip_tags(htmlContent)
        email=EmailMultiAlternatives(
            #subject
            mail_subject,
            #content
            text_content,
            #Sender Email
            settings.EMAIL_HOST_USER,
            #List Of Receiver
            [user.userEmail]
        )
        email.attach_alternative(htmlContent,"text/html")
        email.send()
        
class Page404(TemplateView):
    template_name = "userAuthentication/page404.html"
        
def activate(request, uidb64, token):    
    print("Inside Activation View")
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        myUser = user.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):  
        myUser = None  
    if myUser is not None and account_activation_token.check_token(myUser, token):  
        myUser.activationStatus = True  
        myUser.save()  
        return render(request, "userAuthentication/emailVerification.html", {"emailId": myUser.userEmail})         
    else:  
        pathTo404 = reverse("Page_404", args=["invalidRequest"])
        return HttpResponseRedirect(pathTo404) 
            
