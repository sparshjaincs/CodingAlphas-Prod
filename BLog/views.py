from django.shortcuts import render
from .forms import *
from .models import *
from django.forms.models import model_to_dict
import json
import re
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import date
import datetime
# Create your views here.
def homepage(request):
    
    context = {}
    data = Articles.objects.filter(status = 'Published').order_by("-edited")
    context['carousel'] = data[:1]
    context['side'] = data[1:5]
    context['data'] = data[5:]

    return render(request,'Blog/homepage.html',context)
@login_required
def create(request):
    context = {}
    context['form'] = Article_form()
    context['id'] = 0    
    return render(request,'Blog/create.html',context)

def edit(request,id):
    context = {}
    context['edit'] = True
    instance = Articles.objects.get(id = id)
    if request.user == instance.user:
        context['title'] = instance.title
        context['content'] = instance.content
        context['image'] = instance.image
        context['id'] = id
        context['link'] = instance.image
        context['tags'] = instance.tags
        context['broadcast'] = instance.broadcast
        return render(request,'Blog/edit.html',context)
    else:
        return HttpResponseRedirect('/page_not_found/')

def save(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        title = request.POST.get('title')
        content = request.POST.get('value') 
        instance = request.POST.get('id')
        method = request.POST.get('method')

        if image is not None or title != "" or content != '<p class="ck-placeholder" data-placeholder="Write your story here. Add images or a video for visual impact."><br data-cke-filler="true"></p>' :
            if title == "" or title is None :
                title = "Untitled Draft"
            
            if instance == '0' and method == 'create':
                ins = Articles(user = request.user,image = image,title = title,content = content)
                ins.save()
            else:
                ins = Articles.objects.get(id = instance)
                if image is not None:
                    ins.image = image
                ins.status = 'Drafts'
                ins.title = title
                ins.content = content
                ins.save()
            return HttpResponse(json.dumps({'status':1,"id":ins.id}))
        else:
            return HttpResponse(json.dumps({'status':0}))

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext
def preview_data(request):
    context = {}
    instance = request.GET.get('id')
    instance = Articles.objects.get(id = instance)
    context['image'] = "/media/"+str(instance.image)
    context['title'] = instance.title
    context['desc'] = cleanhtml(instance.content)[:147] + "..."
    context['broadcast'] = instance.broadcast
    context['tags'] = instance.tags
    return HttpResponse(json.dumps(context))

def post(request):
    if request.method == 'POST':
        method = request.POST.get('method')
        tags = request.POST.get('tags')
        public = request.POST.get('public')
        instance = request.POST.get('id')
       
        ins = Articles.objects.get(id = instance)
        ins.tags = tags
        ins.status = method

        if public == "1":
            ins.broadcast = "Public"
        else:
            ins.broadcast = "Private"
        

        ins.save()
        
        if method == 'Published':
            ty = "Published"
        else:
            ty = "Drafts"
        return HttpResponse(json.dumps(f"/profile/{request.user}/?method=Articles&type={ty}"))

def mainpage(request,user,title,id):
    context = {}
    ins = Articles.objects.get(id = id)

    context['data'] = ins
    context['side'] = Articles.objects.filter(user = ins.user, status = "Published").count()
    if ArticleViewCount.objects.filter(article_instance = ins, created = datetime.datetime.strptime(str(date.today()),"%Y-%m-%d")).exists():
        instance = ArticleViewCount.objects.get(article_instance = ins, created = datetime.datetime.strptime(str(date.today()),"%Y-%m-%d"))
        if request.user not in instance.user.all():
            if request.user in User.objects.all():
                instance.count +=1
                instance.user.add(request.user)
                instance.save()
            else:
                instance.count +=1
                instance.save()

            
    else:
        instance = ArticleViewCount(article_instance = ins, count = 1)
        instance.save()

    return render(request,'Blog/mainpage.html',context)

def comment(request):
    if request.method == 'POST':
        data = request.POST.get('value')
        print(data)
    return HttpResponse(json.dumps(""))
@csrf_exempt 
def image_upload(request):
    if request.method == 'POST':
        pass
    return ""


def analytics_data(request):
    aid = request.GET.get('id')
    curr = request.GET.get('index')
    update = request.GET.get('update')
    date_field = []
    view_field = []
    if(int(aid) == -1):
        ins = Articles.objects.filter(user = request.user, status = 'Published').order_by("-id").first()
        
    else:
        ins = Articles.objects.get(user = request.user,id = aid,status='Published')
    instance = ArticleViewCount.objects.filter(article_instance = ins).order_by('-created')[:7]
    for i in instance:
        date_field.append(str(i.created.strftime("%b %d, %Y")))
        view_field.append(i.count)
    while len(date_field) !=7:
        date_field.append("")
        view_field.append(0)
    stack = [ins.like.all().count(),sum([j.count for j in ins.view_count.all()]),ins.bookmark_article.all().count(),ins.blog_comment_ques.all().count()]
    context = {"x":date_field[::-1],"y":view_field[::-1],"title":ins.title,"stack":stack}
    return HttpResponse(json.dumps(context))

def analytics_dataall(request):
    user = request.GET.get("user")
    if user is None:
        user = request.user
    else:
        user = User.objects.get(username = user)
    curr = request.GET.get('index')
    update = request.GET.get('update')
    like_field = 0
    view_field = 0
    title_field = 0
    comment_field=0
    saves_field=0
    ins = Articles.objects.filter(user = user, status = 'Published')
    for i in ins:
    
        like_field += i.like.all().count()
        comment_field += i.blog_comment_ques.all().count()
        saves_field += i.bookmark_article.all().count()
        view_field += sum([j.count for j in i.view_count.all()])
    published_count = ins.all().count()
    draft_count = Articles.objects.filter(user = request.user, status = 'Drafts').all().count()
    context = [like_field,view_field,saves_field,comment_field,published_count,draft_count]
    return HttpResponse(json.dumps(context))