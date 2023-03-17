from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib import messages
from Core.forms import SignUpForm
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, force_text
# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('signinuser')
        password = request.POST.get('siginpassword')

        user = authenticate(username = username,password = password)
        if user is not None:
            if user.profile.signup_confirmation:
                login(request,user)
                return HttpResponseRedirect('/')
            else:
                messages.error(request,"Signup confirmation required!")

                return render(request,'login.html')
        else:

      
            messages.error(request,"Username and Password are Incorrect!")

            return render(request,'login.html')
    else:
        return render(request,'login.html')

def signup(request):
    context = {}
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            try:
                user.username = form.cleaned_data['email'].split("@")[0]
                user.save()
            except:
                context['form'] =  SignUpForm()
                messages.error(request,"Email already exists!")
                return render(request,'signup.html',context)
                
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data['first_name']
            user.profile.last_name = form.cleaned_data['last_name']
            user.profile.email = form.cleaned_data['email']
            user.profile.signup_confirmation = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'noreply@codingalphas.com'
            message = render_to_string('email_template.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        })
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, 'sparshjaincs@gmail.com', [to_email])
            return HttpResponse('Please confirm your email address to complete the registration')
            #raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=user.username, password=raw_password)
            #login(request, user)
            

        else:
            context['form'] =  SignUpForm()
            messages.error(request,form.errors)
            return render(request,'signup.html',context)

    else:
        context['form'] =  SignUpForm()
        return render(request,'signup.html',context)

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user,backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect("/")
    else:
        return HttpResponse('Activation link is invalid!')
    
    