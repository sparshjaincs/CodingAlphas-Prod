from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from BLog.models import Articles, BlogComment
from datetime import datetime
from Discuss.models import Quora
#from ckeditor.fields import RichTextField 
#from ckeditor_uploader.fields import RichTextUploadingField
#from django.contrib.contenttypes.fields import GenericRelation
#from discuss.models import *


class activity(models.Model):
    CHOICE = (
        ('Blog','Blog'),('Post','Post'),('Career','Career'),('Photo','Photo'),('Video','Video'),('discuss','discuss'),('Follow','Follow')
    )
    CHOICES = (
        ('Like','Like'),('Comment','Comment'),('Follow','Follow'),('Photo','Photo'),('Video','Video'),('discuss','discuss'),
    )
    user = models.ForeignKey(User, related_name='user_activity', to_field='username', on_delete=models.CASCADE,default="")
    
    user_activity = models.CharField(max_length=1000,blank=True)
    activity_icon = models.CharField(max_length=200,blank=True)
    created= models.DateTimeField(auto_now_add=True,null=True)
    category = models.CharField(max_length=1000,choices = CHOICE,default="Blog")
    choice = models.CharField(max_length=1000,choices = CHOICES,default="Like")
    another = models.ForeignKey(User,related_name = "activity_user",on_delete = models.CASCADE,null=True,blank=True)
    article_instance = models.ForeignKey(Articles, related_name='user_activity_acticles', on_delete=models.CASCADE,default="",blank=True,null=True)
    article_comment_instance = models.ForeignKey(BlogComment, related_name='user_activity_article_comment',  on_delete=models.CASCADE,default="",null=True,blank=True)
    def __str__(self):
        return f'{self.user}  -- > Activty {self.user_activity}'
class Activity_Counter(models.Model):
    user =  models.ForeignKey(User, related_name='user_activity_counter', to_field='username', on_delete=models.CASCADE,default="")
    ins_act = models.ManyToManyField(activity,related_name="activity_instance",default="")
    counter = models.IntegerField(blank=True, null=True,default=0)
    status = models.CharField(max_length = 100, choices = (('unread','unread'),('read','read')),default='unread')
    balance = models.IntegerField(blank = True, null = True, default=0)
    def __str__(self):
        return self.user.username
@receiver(post_save, sender=activity)
def update_counter(sender, instance, created, **kwargs):
    if created:
        if Activity_Counter.objects.filter(user = instance.user).exists():
            ins = Activity_Counter.objects.get(user = instance.user)
            ins.ins_act.add(instance)
            ins.counter = ins.counter + 1
            ins.status = 'unread'
            ins.save()
      

 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True,default="")
    last_name = models.CharField(max_length=50, blank=True,default="")
    email = models.EmailField(max_length=50, blank=True,default="")
    phone_number = models.CharField(max_length=13, blank=True,default="")
    avatar = models.ImageField(upload_to='users/images',blank=False,default = 'users/images/default.jpg')
    cover = models.ImageField(upload_to='cover/images',blank=False,default = 'cover/images/default.jpg')
    headline = models.CharField(max_length=1000, blank=True,default="")
    bio = models.TextField(blank=True,default="")
    work = models.CharField(max_length=50, blank=True,default="")
    address = models.CharField(max_length=50, blank=True,default="")
    city = models.CharField(max_length=50, blank=True,default="")
    state  = models.CharField(max_length=50, blank=True,default="")
    country = models.CharField(max_length=50, blank=True,default="")
    date_of_birth = models.CharField(max_length=13, blank=True,default="")
    followers = models.ManyToManyField(User,default=None,blank=True,related_name="follow_title")
    following = models.ManyToManyField(User,default=None,blank=True,related_name="following_title")
    signup_confirmation = models.BooleanField(default=False)
    instagram = models.CharField(max_length=1000,blank=True,null=True)
    website = models.CharField(max_length=1000,blank=True,null=True)
    linkedin = models.CharField(max_length=1000,blank=True,null=True)
    github = models.CharField(max_length=1000,blank=True,null=True)
    facebook = models.CharField(max_length=1000,blank=True,null=True)
    twitter = models.CharField(max_length=1000,blank=True,null=True)
    college = models.CharField(max_length=1000, blank=True,default="")
    medium = models.CharField(max_length=1000,blank=True,null=True)
    quora = models.CharField(max_length=1000,blank=True,null=True)
    youtube = models.CharField(max_length=1000,blank=True,null=True)
    other = models.CharField(max_length=1000,blank=True,null=True)
    education = models.CharField(max_length=1000, blank=True,default="")
    subscribe = models.ManyToManyField(User,default=None,blank=True,related_name="subscribe_title")
    mute = models.ManyToManyField(User,default=None,blank=True,related_name="mute_title")
    gender = models.CharField(max_length=100,choices = (('Male','Male'),('Female','Female'),('Other','Other')),default = 'Male')
    important_announcement = models.BooleanField(default=True)
    feature_announcement = models.BooleanField(default=True)
    weekly_recommendation = models.BooleanField(default=True)
    articles_updates = models.BooleanField(default=True)
    thanksgiving_promotion = models.BooleanField(default=True)
    other_promotion = models.BooleanField(default=True)
    email_notification = models.BooleanField(default=True)
    
  
    

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        #instance.username = instance.email.split("@")[0]
        #instance.save()
        Profile.objects.create(user=instance)
        ins = Activity_Counter(user = instance,counter = 0)
        ins.save()
        

    instance.profile.save()

    




            
        
            
    

class Photo(models.Model):
    user = models.ForeignKey(User,related_name="photo_user",on_delete=models.CASCADE,to_field="username")
    description = models.CharField(max_length=10000,blank = False)
    tags = models.CharField(max_length=1000,blank = True,null = True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    like = models.ManyToManyField(User,default=None,blank=True,related_name="photo_like")
    dislike = models.ManyToManyField(User,default=None,blank=True,related_name="photo_dislike")
    def __str__(self):
        return self.user.username
class Photo_Image(models.Model):
    instance = models.ForeignKey(Photo,related_name="photo_image",on_delete=models.CASCADE)
    image = models.ImageField(upload_to='users/images',blank=False)
    def __str__(self):
        return self.instance.user.username

class Video(models.Model):
    user = models.ForeignKey(User,related_name="video_user",on_delete=models.CASCADE,to_field="username")
    description = models.CharField(max_length=10000,blank = False)
    tags = models.CharField(max_length=1000,blank = True,null = True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    video_file = models.FileField(upload_to='users/videos', null=True, verbose_name="")
    like = models.ManyToManyField(User,default=None,blank=True,related_name="video_like")
    dislike = models.ManyToManyField(User,default=None,blank=True,related_name="video_dislike")
    def __str__(self):
        return self.user.username

class Post(models.Model):
    user = models.ForeignKey(User,related_name="post_user",on_delete=models.CASCADE,to_field="username")
    description = models.TextField(blank = False, null = False)
    tags = models.CharField(max_length=1000,blank = True,null = True)
    video_file = models.FileField(upload_to='users/videos', null=True, verbose_name="",blank = True)
    attachment = models.FileField(upload_to='users/attachments', null=True, verbose_name="",blank = True)
    gifs = models.FileField(upload_to='users/gifs', null=True, verbose_name="",blank = True)
    like = models.ManyToManyField(User,default=None,blank=True,related_name="post_like")
    dislike = models.ManyToManyField(User,default=None,blank=True,related_name="posr_dislike")
    created = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.user.username
    @property
    def extension(self):
        name, extension = os.path.splitext(self.attachment.name)
        return extension
class Post_Image(models.Model):
    instance = models.ForeignKey(Post,related_name="post_image",on_delete=models.CASCADE)
    image = models.ImageField(upload_to='users/images',blank=False)
    def __str__(self):
        return self.instance.user.username

    
class Homepage_Activity(models.Model):
    CHOICE = (
        ('Blog','Blog'),('Post','Post'),('Career','Career'),('Photo','Photo'),('Video','Video'),('discuss','discuss'),
    )
    user = models.ForeignKey(User,related_name="homepage_user",on_delete=models.CASCADE,to_field="username",default="Admin")
    
    category = models.CharField(max_length=1000,choices = CHOICE)
    blog = models.ForeignKey(Articles,related_name = "homepage_blog",on_delete = models.CASCADE,null=True,blank=True)
    post = models.ForeignKey(Post,related_name = "homepage_post",on_delete = models.CASCADE,null=True,blank=True)
    photo = models.ForeignKey(Photo,related_name = "homepage_photo",on_delete = models.CASCADE,null=True,blank=True)
    video = models.ForeignKey(Video,related_name = "homepage_video",on_delete = models.CASCADE,null=True,blank=True)
    discuss = models.ForeignKey(Quora,related_name = "homepage_discuss",on_delete = models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.category



class Bookmark(models.Model):
    CHOICE = (
        ('Blog','Blog'),('Post','Post'),('Career','Career'),('Photo','Photo'),('Video','Video'),('discuss','discuss'),
    )
    user = models.ForeignKey(User,related_name='bookmarkuser',on_delete=models.CASCADE,to_field='username')
    category = models.CharField(max_length=100, choices=CHOICE,default='Blog')
    article_instance = models.ManyToManyField(Articles,related_name="bookmark_article")
    def __str__(self):
        return self.user.username

    def bookmarkArticles(self):
        return self.article_instance.all()






 




 