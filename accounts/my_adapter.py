from django.contrib.auth.models import User

#from allauth.account.models import EmailAccount
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
import requests
import tempfile
from django.core import files

def download_file(url):
    try:
        request = requests.get(url = url, stream = True)
    except requests.exceptions.RequestException as e:
        return None
    if request.status_code != requests.codes.ok:
        return None
    lf = tempfile.NamedTemporaryFile()
    for block in request.iter_content(1024*8):
        if not block:
            break
        lf.write(block)
    return files.File(lf)

class MyAdapter(DefaultSocialAccountAdapter):
    
    def save_user(self,request, sociallogin, form = None):
        try:
            user = super(MyAdapter, self).save_user(request, sociallogin, form)
            
            url = sociallogin.account.get_avatar_url()
            avatar = download_file(url)
            profile = user.profile
            if avatar:
                

                profile.avatar.save('avatar%d.jpg'%user.pk, avatar)
                
            profile.first_name = user.first_name
            profile.last_name = user.last_name
            profile.email = user.email
            profile.save()
            
            
            return user
        except:
            pass