from django.shortcuts import render , redirect
from .models import Profile
from django.http import HttpResponse
from django.contrib.auth.models import User
import random
import http.client
from django.conf import settings

# Create your views here.
def SendOTPies(mobile , otp):
  conn = http.client.HTTPSConnection("api.msg91.com")
  authkey=settings.AUTH_KEY
  headers = { 'content-type': "application/json" }
  url = "http//:control.msg91.com/apisendotp.php?otp="+otp+'&sender=abc&message='+'Your otp is '+otp+'&mobile='+mobile+'&authkey='+authkey+'&country=91'
  conn.request("GET",url,"/api/v5/otp?template_id=&mobile=&authkey=", headers=headers)
  res = conn.getresponse()
  data = res.read()
  print(data)
  return None

  

def register(request):
 if request.method == 'POST':
      email=request.POST.get('email')
      name=request.POST.get('name')
      mobile=request.POST.get('mobile')

      check_user=User.objects.filter(email = email).first()
      check_profile=Profile.objects.filter(mobile = mobile).first()

      if check_user  or check_profile:
         context={'message':'User  Already exists', 'class':'danger'}
         return render(request , 'enroll/register.html' , context)

      user=User(email = email , first_name =name)
      user.save()
      otp=str(random.randint(1000,9999))
      profile=Profile(user = user , mobile = mobile , otp = otp)
      profile.save()
      SendOTPies(mobile , otp)
      request.session['mobile']=mobile  # call hone ke bad
      return redirect ('otps')
 return render(request , 'enroll/register.html')


def otp(request):
  mobile = request.session['mobile'] 
  context = {'mobile':mobile} 
  if request.method=='POST':
    otp=request.POST.get('otp')
    profile=Profile.objects.filter(mobile=mobile).first()
    if otp==profile.otp:
      return redirect('')
    else:
      context={'message':'Wrong otp', 'class':'danger','mobile':mobile}
      return render(request ,'enroll/register.html' , context)
       
  return render(request , 'enroll/otp.html' ,context)





def Login(request):
  return render(request , 'enroll/login.html')
