from django.shortcuts import render
from .forms import *
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import PasswordResetView

from django.http import HttpResponse, HttpResponseRedirect
from BLog.models import Articles, BlogComment
from django.contrib import messages
from .news import *
import json
from datetime import date
from .models import *
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
import re
# Create your views here.
def homepage(request):
    context = {}
    context['blogs'] = Articles.objects.filter(status = 'Published').order_by("-edited")[2:7]
    if request.user.is_authenticated:
        context['home'] = Homepage_Activity.objects.all().order_by('-id')
        context['day'] = date.today()
        context['activity'] = activity.objects.filter(user = request.user).order_by('-id')[:5]
        
        feed = ParseFeed('Coding')
        data = feed.parse()
        context['news'] = data[:6]
        
        return render(request,"Core/homepage.html",context)
    else:
        context['blogs'] = Articles.objects.filter(status = 'Published').order_by("-edited")
        return render(request,'Core/landing.html',context)
    

def coming_soon(request):
    return render(request,'Core/comming_soon.html')

def signingup(request):
    context = {}
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = form.cleaned_data['email'].split("@")[0]
            user.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data['first_name']
            user.profile.last_name = form.cleaned_data['last_name']
            user.profile.email = form.cleaned_data['email']
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/')

        else:
            messages.error(request,form.errors)
            return render(request,'Core/snippets/signup.html',context)

    else:
        context['form'] =  SignUpForm()
        return render(request,'Core/snippets/signup.html',context)
    

def profile(request,user):
    context = {}
    context['user'] = User.objects.get(username = user)
    method = request.GET.get('method')
    context['profile'] = Profile.objects.get(user = context['user'])
    if method is None or method == "Dashboard":
        context['method'] = "Dashboard"
        context['data'] = Articles.objects.filter(user = context['user'], status="Published").order_by("-id")[:5]
        context['activities'] = activity.objects.filter(user = context['user']).order_by('-id')[:5]
        context['counter'] = Activity_Counter.objects.filter(user = request.user)
    elif method == "Timeline":
        context['home'] = Homepage_Activity.objects.filter(user =  context['user']).order_by('-id')
        context['method'] = 'Timeline'
    elif method == 'Notifications':
        t = request.GET.get('type')
        context['counter'] = Activity_Counter.objects.filter(user = request.user)
        sort = request.GET.get('sort')
        if sort is None or sort == 'asc':
            sort = 'desc'
        else:
            sort = 'asc'
        if t is None or t == 'All': 
            context['type'] = 'All'
            if sort == 'desc' :
                context['notify'] = activity.objects.filter(user = request.user ).order_by('-id')
            else:
                context['notify'] = activity.objects.filter(user = request.user).order_by('id')
        else:
            context['type'] = t
        context['sort'] = sort
        context['method'] = 'Notifications'
    elif method == 'Articles':
        category = request.GET.get('type')
        if category is None:
            category = 'Published'
        if request.user == context['user']: 
            context['data'] = Articles.objects.filter(user = context['user'],status = category).order_by('-date')
            context['count'] = len(context['data'])
            context['alter'] = context['user'].project_username_2.all().count() - context['count']
        elif category == 'Drafts' and request.user != context['user']:
            context['panitrate'] = True
        context['method'] = method
        context['type'] = category
    elif method == 'Bookmarks':
        articles_flag = False
        if Bookmark.objects.filter(user = request.user).exists():
            bookins = Bookmark.objects.get(user = request.user)
            if bookins.article_instance.all().count() != 0:
                articles_flag = True
            context['bookins'] = bookins

        context['article_flag'] = articles_flag
        
        context['method'] = 'Bookmarks'
    elif method == 'BookmarksExtend':
        t = request.GET.get('type')
        if t == 'Articles':
            context['extend'] = Bookmark.objects.get(user = request.user).bookmarkArticles()
        context['method'] = 'BookmarksExtend'
    elif method == 'Setting':
        t = request.GET.get('type')
        if t == 'basic' or t is None:
            context['type'] = 'basic'
        else:
            context['type'] = t
        context['method'] = 'Setting'
    elif method == 'Statistics':
        context['data'] = Articles.objects.filter(user = request.user, status = 'Published').order_by('-id')
        context['method'] = 'Statistics'
    elif method == 'Connections':
        t = request.GET.get('type')
        if t is None or t == 'followers':
            context['type'] = 'followers'
        elif t == 'suggested':
            context['users'] = User.objects.all()
            context['type'] = 'suggested'
        else:
            context['type'] = t
        context['method'] = 'Connections'
    else:
        context['method'] = method

    
   
    return render(request,'Core/profile.html',context)

def photo_upload(request):
    if request.method == 'POST':
        data = request.FILES.getlist('photo_files')
        text = request.POST.get('photo_text')
        tags = request.POST.get('photo_taggs')
        ins = Photo(user = request.user,description = text,tags = tags)
        ins.save()
        for i in data:
            ins1 = Photo_Image(instance = ins,image = i)
            ins1.save()
        ins1 = Homepage_Activity(user=request.user,category = 'Photo',photo = ins)
        ins1.save()
        ins2 = activity(user = request.user,activity_icon = "fa fa-cloud-upload",user_activity=f"You have shared a <a href='/activities/photo/{ins.id}/'>photo</a>.")
        ins2.save()
        return HttpResponse(json.dumps("Success"))
    else:
        return HttpResponse(json.dumps("Error"))


def video_upload(request):
    if request.method == 'POST':
        data = request.FILES.get('video_file')
        text = request.POST.get('video_text')
        tags = request.POST.get('video_tags')
        ins = Video(user = request.user,description = text,tags = tags,video_file = data)
        ins.save()
        ins1 = Homepage_Activity(user=request.user,category = 'Video',video = ins)
        ins1.save()
        ins2 = activity(user = request.user,activity_icon = "fa fa-cloud-upload",user_activity=f"You have shared a <a href='/activities/video/{ins.id}/'>video</a>.")
        ins2.save()
        content={
            'name':ins.user.profile.first_name +" "+ins.user.profile.last_name,
            'user':ins.user.username,
            'uid':ins.id,
            'desc':ins.description,
            'tags':ins.tags,
            'video':str(ins.video_file.url),
            'time':ins.created.strftime("%B %d, %Y, %H:%M %p"),
            'photo':str(ins.user.profile.avatar.url),

        }
        return HttpResponse(json.dumps(("Success",content), cls=DjangoJSONEncoder))
    else:
        return HttpResponse(json.dumps(("Error")))

def post_upload(request):
    if request.method == 'POST':
        text = request.POST.get('editor1')
        tags = request.POST.get('post_tags')
        image = request.FILES.getlist('post_photo_files')
        video = request.FILES.get('post_video_file')
        document = request.FILES.get('post_doc_file')
    
        ins = Post(user = request.user,description = text,tags = tags,video_file = video,attachment = document)
        ins.save()
        for i in image:
            ins1 = Post_Image(instance = ins,image = i)
            ins1.save()
        ins1 = Homepage_Activity(user=request.user,category = 'Post',post = ins)
        ins1.save()
        ins2 = activity(user = request.user,activity_icon = "fa fa-cloud-upload",user_activity=f"You have shared a <a href='/activities/post/{ins.id}/'>post</a>.")
        ins2.save()
        return HttpResponse(json.dumps("Success"))
    else:
       return HttpResponse(json.dumps("Error"))

def settings(request):
    return render(request,'Core/settings.html')




def activities(request,method,value):
    return render(request,'Core/activities.html')



def news(request,topic):
    context = {}
    feed = ParseFeed(topic)
    data = feed.parse()
    context['data'] = data
   
    context['method'] = topic
    return render(request,'Core/news.html',context)
def ajax_news(request):
    topic = request.GET.get('topic').replace(" ","-")
    feed = ParseFeed(topic)
    data = feed.parse()
    return HttpResponse(json.dumps(data))


def like(request):
    method = request.GET.get('method')
    instance = request.GET.get('instance')
    if method == 'blog':
        ins = Articles.objects.get(id = instance)
        if request.user in ins.like.all():
            ins.like.remove(request.user)
            status = 0
        else:
            ins.like.add(request.user)
            status = 1
            title = ins.title.replace(" ","-")
            info = f"<a href='/profile/{request.user}/'>{request.user.profile.first_name} {request.user.profile.last_name}</a> liked your <a data-toggle='tooltip' title='Read Article' href='/blogs/read/{ins.user}/{title}/{ins.id}/'>article</a>."
            act = activity(user = ins.user, user_activity = info, article_instance = ins ,activity_icon = 'fa fa-heart', category='Blog',another=request.user, choice = 'Like')
            act.save()
        likecount = ins.like.all().count() 
    elif method == "blog_comment":
        ins = BlogComment.objects.get(id = instance)
        if request.user in ins.like.all():
            ins.like.remove(request.user)
            status = 0
        else:
            ins.like.add(request.user)
            status = 1
            title = ins.question.title.replace(" ","-")
            info = f"<a href='/profile/{request.user}/'>{request.user.profile.first_name} {request.user.profile.last_name}</a> liked your <a data-toggle='tooltip' title='Read Comment' href='/blogs/read/{ins.question.user}/{title}/{ins.question.id}/#comment_class'>comment</a> : {ins.body}"
            act = activity(user = ins.user, article_instance = ins.question , article_comment_instance = ins,user_activity = info, activity_icon = 'fa fa-heart', category='Blog',another=request.user, choice = 'Like')
            act.save()
        likecount = ins.like.all().count() 
    elif method == 'discuss':
        ins = Quora.objects.get(id = instance)
        if request.user in ins.like.all():
            ins.like.remove(request.user)
            status = 0
        else:
            ins.like.add(request.user)
            if request.user in ins.dislike.all():
                ins.dislike.remove(request.user)
            status = 1
        likecount = ins.like.all().count()  
        dislikecount = ins.dislike.all().count()
    elif method == 'discussanwser':
        ins = AnsModel.objects.get(id=instance)
        if request.user in ins.like.all():
            ins.like.remove(request.user)
            status = 0
        else:
            ins.like.add(request.user)
            if request.user in ins.dislike.all():
                ins.dislike.remove(request.user)
            status = 1  
        likecount = ins.like.all().count()  
        dislikecount = ins.dislike.all().count()
    elif method == 'discusscomment':
        ins = CommentSystem.objects.get(id=instance)
        if request.user in ins.like.all():
            ins.like.remove(request.user)
            status = 0
        else:
            ins.like.add(request.user)
            if request.user in ins.dislike.all():
                ins.dislike.remove(request.user)
            status = 1  
        likecount = ins.like.all().count()  
        dislikecount = ins.dislike.all().count()
    elif method == 'post':
        ins = Post.objects.get(id = instance)
        if request.user in ins.like.all():
            ins.like.remove(request.user)
            status = 0
        else:
            ins.like.add(request.user)
            if request.user in ins.dislike.all():
                ins.dislike.remove(request.user)
            status = 1
        likecount = ins.like.all().count()  
        dislikecount = ins.dislike.all().count()



    return HttpResponse(json.dumps([status,likecount]))


def dislike(request):
    method = request.GET.get('method')
    instance = request.GET.get('instance')
    if method == 'discuss':
        ins = Quora.objects.get(id = instance)
        if request.user in ins.dislike.all():
            ins.dislike.remove(request.user)
            status = 0
        else:
            ins.dislike.add(request.user)
            if request.user in ins.like.all():
                ins.like.remove(request.user)
            status = 1
        dislikecount = ins.dislike.all().count()
        likecount = ins.like.all().count() 
    elif method == 'discussanwser':
        ins = AnsModel.objects.get(id = instance)
        if request.user in ins.dislike.all():
            ins.dislike.remove(request.user)
            status = 0
        else:
            ins.dislike.add(request.user)
            if request.user in ins.like.all():
                ins.like.remove(request.user)
            status = 1
        dislikecount = ins.dislike.all().count()
        likecount = ins.like.all().count() 
    elif method == 'discusscomment':
        ins = CommentSystem.objects.get(id = instance)
        if request.user in ins.dislike.all():
            ins.dislike.remove(request.user)
            status = 0
        else:
            ins.dislike.add(request.user)
            if request.user in ins.like.all():
                ins.like.remove(request.user)
            status = 1
        dislikecount = ins.dislike.all().count()
        likecount = ins.like.all().count() 
    elif method == 'post':
        ins = Post.objects.get(id = instance)
        if request.user in ins.dislike.all():
            ins.dislike.remove(request.user)
            status = 0
        else:
            ins.dislike.add(request.user)
            if request.user in ins.like.all():
                ins.like.remove(request.user)
            status = 1
        likecount = ins.like.all().count()  
        dislikecount = ins.dislike.all().count()
    return HttpResponse(json.dumps([status,str(dislikecount)+" Dislikes",str(likecount)+" Likes"]))


def follow(request):
    us = request.GET.get('method')
   
    ins = User.objects.get(username = us)

    if ins != request.user:
        if request.user in ins.profile.followers.all():
            ins.profile.followers.remove(request.user)
            status = 0
        else:
            ins.profile.followers.add(request.user)
            status = 1
            text = f"<a href='/profile/{request.user}/'>{request.user.profile.first_name} {request.user.profile.last_name}</a> started following you"
            instance = activity(user = ins, user_activity = text, activity_icon = "fa fa-user-plus", category='Follow', choice = 'Follow', another = request.user)
            instance.save()
        if ins in request.user.profile.following.all():
            request.user.profile.following.remove(ins)
        else:
            request.user.profile.following.add(ins)
    else:
        status = 2 
    return HttpResponse(json.dumps([status,ins.profile.first_name + " " + ins.profile.last_name]))

def mark(request):
    method = request.GET.get('method')
    instance = request.GET.get('ins')
    if method == 'blog':
        ins = Articles.objects.get(id = instance)
        if Bookmark.objects.filter(user = request.user).exists():
            bookins = Bookmark.objects.get(user = request.user)
        else:
            bookins = Bookmark(user = request.user)
            bookins.save()

        if ins in bookins.article_instance.all():
            bookins.article_instance.remove(ins)
            status = 0
        else:
            bookins.article_instance.add(ins)
            status = 1
    if method == 'discuss':
        instance = Profile.objects.get(user = request.user)
        ins = Quora.objects.get(id = ins)
        if ins in instance.quora_discuss.all():
            instance.quora_discuss.remove(ins)
            status = 0
        else:
            instance.quora_discuss.add(ins)
            status = 1
    

    return HttpResponse(json.dumps([status]))

def comment_submit(request):
    if request.method == 'POST':
        type= request.POST.get("type")
        instance= request.POST.get("instance")
        text = request.POST.get("text")
        method= request.POST.get("method")
        comment_instance= request.POST.get("comment_instance")
        status = 0
        if type == "blog":
            ins = Articles.objects.get(id = instance)
            title = ins.title.replace(" ","-")
            if method == "parent":
                blog_ins = BlogComment(user = request.user, question = ins, body = text)
                blog_ins.save()
                status = 1
                info = f"<a href='/profile/{request.user}/'>{request.user.profile.first_name} {request.user.profile.last_name}</a> commented on your<a data-toggle='tooltip' title='Read Article' href='/blogs/read/{ins.user}/{title}/{ins.id}/'> article </a>: {text} "
           
            elif method == "child":
                blog_parent = BlogComment.objects.get(id = comment_instance)
                info = f"<a href='/profile/{request.user}/'>{request.user.profile.first_name} {request.user.profile.last_name}</a> mentioned you in a comment of an<a data-toggle='tooltip' title='Read Article' href='/blogs/read/{ins.user}/{title}/{ins.id}/'> article </a>: {text}"
           
                text = f"<a href='/profile/{blog_parent.user}/' style='font-size:13px; font-weight:600;'>@{blog_parent.user.profile.first_name} {blog_parent.user.profile.last_name} </a> " + text
                blog_ins = BlogComment(user = request.user,question=ins, body = text, parent = blog_parent)
                blog_ins.save()
                status = 1
                
            
            act = activity(user = ins.user, user_activity = info, article_instance = ins , article_comment_instance = blog_ins ,activity_icon = 'fa fa-comment', category='Blog',another=request.user,choice='Comment')
            act.save()
    

    return HttpResponse(json.dumps(status))

def notification_balance(request):
    ins = Activity_Counter.objects.get(user = request.user)
    l = []
    data = activity.objects.filter(user = request.user).order_by('-id')[:10]
    for i in data:
        context = {}
        if i in ins.ins_act.all():
            context['new'] = True
        else:
            context['new'] = False
        context['image'] = str(i.another.profile.avatar)
        context['category'] = i.category
        context['created'] = str(i.created.strftime("%b %d,%Y, %H:%M %p"))
        context['activity'] = i.user_activity
        l.append(context)


        
    

    ins.counter = 0
    ins.status = 'read'
    for i in ins.ins_act.all():
        ins.ins_act.remove(i)
    ins.save()
    return HttpResponse(json.dumps([1,l]))

def delete(request):
    if request.method == 'GET':
        status = 0
        method = request.GET.get('method')
        instance = request.GET.get("ins")
        if method == 'activity':
            try:
                ins = activity.objects.get(id = instance)
                ins.delete()
                status = 1
            except:
                status = 0
        elif method == 'comment_delete':
            try:
                ins = BlogComment.objects.get(id = instance)
                ins.delete()
                status = 1
            except:
                status = 0
        elif method == 'blog':
            try:
                ins = Articles.objects.get(id = instance)
                ins.delete()
                status = 1
            except:
                status = 0
    return HttpResponse(json.dumps(status))

@csrf_exempt
def profiledata(request):
    status = 0
    info = ""
    pattern=r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
    if request.method == 'POST':
        method = request.POST.get("method")
        value = request.POST.get("value")
        user = request.user
        profile = Profile.objects.get(user = user)
        if method == 'name':
            arr = value.split(" ")
            if len(arr) == 1 :
                profile.first_name = value
                profile.last_name =""
                profile.save()
            elif len(arr) == 2 :
                profile.first_name = arr[0]
                profile.last_name = arr[1]
                profile.save()
            
            else:
                profile.first_name = " ".join(arr[:-1]) 
                profile.last_name = arr[-1]
                profile.save()
            
            
            
            status = 1
        elif method == 'title':
            profile.headline = value
            profile.save()
            status = 1
        elif method == 'about':
            profile.bio = value
            profile.save()
            status = 1
        elif method == 'website':
            profile.website = value
            profile.save()
            value = f"<a href='{value}'>"+value+"</a>"
            status = 1
        elif method == 'date':
            arr = value.split("-")
            month =['January','February','March','April','May','June','July','August','September','October','November','December']
            value = f"{month[int(arr[1])-1]} {arr[2]}, {arr[0]}"
            profile.date_of_birth = value
            profile.save()
            status = 1
        elif method == 'gender':
            profile.gender = value
            profile.save()
            status = 1
        elif method == 'work':
            profile.work = value
            profile.save()
            status = 1
        elif method == 'education':
            profile.education = value
            profile.save()
            status = 1
        elif method == 'contact':
            r = re.match(r"^([789][0-9]{9})$",value)
            if r:
                profile.phone_number = value
                profile.save()
                status = 1
            else:
                info = "Please match the requested format ( 10 digits phone number)"
                status = 0
        elif method == 'facebook':
            r = re.match(pattern,value)
            if r:
                profile.facebook = value
                profile.save()
                status = 1
            else:
                info = "Please match the requested format ( 10 digits phone number)"
                status = 0
        elif method == 'instagram':
            r = re.match(pattern,value)
            if r:
                profile.instagram = value
                profile.save()
                status = 1
            else:
                info = "Please match the requested format ( 10 digits phone number)"
                status = 0
        elif method == 'twitter':
            r = re.match(pattern,value)
            if r:
                profile.twitter = value
                profile.save()
                status = 1
            else:
                info = "Please match the requested format ( 10 digits phone number)"
                status = 0
        elif method == 'medium':
            r = re.match(pattern,value)
            if r:
                profile.medium = value
                profile.save()
                status = 1
            else:
                info = "Please match the requested format ( 10 digits phone number)"
                status = 0
        elif method == 'quora':
            r = re.match(pattern,value)
            if r:
                profile.quora = value
                profile.save()
                status = 1
            else:
                info = "Please match the requested format ( 10 digits phone number)"
                status = 0
        elif method == 'linkedin':
            r = re.match(pattern,value)
            if r:
                profile.linkedin = value
                profile.save()
                status = 1
            else:
                info = "Please match the requested format ( 10 digits phone number)"
                status = 0
        elif method == 'profileimage':
            image = request.FILES.get('file')
            profile.avatar = image
            profile.save()
            status=1
    else:
        profile = Profile.objects.get(user = request.user)
        method = request.GET.get('method')
        value=""
        if method == 'important':
            if profile.important_announcement:
                profile.important_announcement = False
                profile.save()
                
            else:
                profile.important_announcement = True
                profile.save()
            status = 1
        elif method == 'feature':
            if profile.feature_announcement:
                profile.feature_announcement = False
                profile.save()
                
            else:
                profile.feature_announcement = True
                profile.save()
            status = 1
        elif method == 'weekly':
            if profile.weekly_recommendation:
                profile.weekly_recommendation = False
                profile.save()
                
            else:
                profile.weekly_recommendation = True
                profile.save()
            status = 1
        elif method == 'articles':
            if profile.articles_updates:
                profile.articles_updates = False
                profile.save()
                
            else:
                profile.articles_updates = True
                profile.save()
            status = 1
        elif method == 'email':
            if profile.email_notification:
                profile.email_notification = False
                profile.save()
                
            else:
                profile.email_notification = True
                profile.save()
            status = 1
        elif method == 'thanks':
            if profile.thanksgiving_promotion:
                profile.thanksgiving_promotion = False
                profile.save()
                
            else:
                profile.thanksgiving_promotion = True
                profile.save()
            status = 1
        elif method == 'other':
            if profile.other_promotion:
                profile.other_promotion = False
                profile.save()
                
            else:
                profile.other_promotion = True
                profile.save()
            status = 1
        elif method == 'retrieve':
            value = str(profile.avatar)
            status = 1


        
    return HttpResponse(json.dumps([status,value, info]))