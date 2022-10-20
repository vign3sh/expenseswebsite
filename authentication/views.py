from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from pandas import reset_option
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .utils import account_activation_token
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.tokens import  PasswordResetTokenGenerator
# Create your views here.


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry email in use,choose another one '}, status=409)
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry username in use,choose another one '}, status=409)
        return JsonResponse({'username_valid': True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
		# GET USER DATA
        # VALIDATE
        # create a user account

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }

                link = reverse('activate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})

                email_subject = 'Activate your account'

                activate_url = 'http://'+current_site.domain+link

                email = EmailMessage(
                    email_subject,
                    'Hi '+user.username + ', Please the link below to activate your account \n'+activate_url,
                    'noreply@semycolon.com',
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, 'Account successfully created')
                return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                messages.success(request, 'User already activated')
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' +
                                     user.username+' you are now logged in')
                    return redirect('expenses')
                messages.error(
                    request, 'Account is not active,please check your email')
                return render(request, 'authentication/login.html')
            messages.error(
                request, 'Invalid credentials,try again')
            return render(request, 'authentication/login.html')

        messages.error(
            request, 'Please fill all fields')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')
		
class RequestResetPasswordEmail(View):
    def get(self, request):
        return render(request,'authentication/reset-password.html')

    def post(self, request):
        email=request.POST['email']
        
        context={
            'values':request.POST
        }

        if not validate_email(email):
            messages.error(request, 'Please enter a valid email')
            return render(request,'authentication/reset-password.html',context)
        
        current_site = get_current_site(request)
        user=User.objects.filter(email=email)
   

        if user.exists():
            messages.success(request, 'We have sent you the email')
            email_contents = {
                'user': user[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0]),
            }

            link = reverse('reset-user-password', kwargs={
                            'uidb64': email_contents['uid'], 'token': email_contents['token']})

            email_subject = 'Password Reset Link'

            reset_url = 'http://'+current_site.domain+link

            email = EmailMessage(
                email_subject,
                'Hi there, Please click the link below to reset your password \n'+reset_url,
                'noreply@semycolon.com',
                [email],
            )
            email.send(fail_silently=False)
            return render(request,'authentication/reset-password.html',context)

        else:
            messages.error(request, 'Email not found')
            return render(request,'authentication/reset-password.html',context)


class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        return render(request,'authentication/set-new-password.html',context)

    def post(self, request, uidb64, token):
        context={
            'uidb64':uidb64,
            'token':token
        }

        password=request.POST['password']
        password2=request.POST['password2']

        if (password != password2):
            messages.error(request, 'Passwords do not match')
            return render(request,'authentication/set-new-password.html',context)
        

        if (len(password)<6):
            messages.error(request, 'Password too short, should be atleast 6 characters')
            return render(request,'authentication/set-new-password.html',context)
        
        
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.error(request, 'Password link is invalid, please request a new link')
                return render(request,'authentication/reset-password.html')
                
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset successfully, you can login with new credentials')
            return redirect('login')
            
        except Exception as identifier:
            messages.info(request,'Something went wrong, try again')
            return render(request,'authentication/set-new-password.html',context)

        