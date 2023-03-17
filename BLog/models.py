from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField 
from ckeditor_uploader.fields import RichTextUploadingField
import re 
from datetime import date
from django.utils import timezone 
# Create your models here. 

   
class Articles(models.Model):
    STATUS_CHOICES = (
		("Drafts", "Drafts"),("Published", "Published"),)
    BROADCAST_CHOICES = (
		('Public', 'Public'),('Private', 'Private'),)
    user = models.ForeignKey(User, related_name='project_username_2', to_field='username', on_delete=models.CASCADE)
    title = models.TextField(max_length = 10000,default=" ",blank=True,unique=False, null=True)
    date = models.DateTimeField(auto_now_add = True)
    edited = models.DateTimeField(auto_now = True)
    image = models.ImageField(upload_to='users/images',blank=True,null=True,default="/users/images/undraw_developer_activity_bv83_1HLxfQZ.svg/")
    content = RichTextUploadingField(null=True)
    description = models.TextField(blank=True,default="")
    tags = models.CharField(max_length=300,blank=True,default="",null=True,help_text='Add comma( ,) seperated tags!!')
    status = models.CharField(max_length=30,choices=STATUS_CHOICES,default='Drafts')
    broadcast = models.CharField(max_length=10,choices=BROADCAST_CHOICES,default='Public')
    like = models.ManyToManyField(User,default=None,blank=True,related_name="likes_title")
    dislike = models.ManyToManyField(User,default=None,blank=True,related_name="dislikes_title")
    bookmark = models.ManyToManyField(User,default=None,blank=True,related_name="bookmark_title")
    class Meta:
        ordering = ['-id']
    def __str__(self):
        return str(self.title)
    @property
    def num_likes(self):
        return self.like.all().count()

    @property
    def num_dislikes(self):
        return self.dislike.all().count()
    def __init__(self, *args, **kwargs):
        super(Articles, self).__init__(*args, **kwargs)
        self._date = self.date
    
    def save(self, *args, **kwargs):
        if not self._date and self.date:
            self.edited = django.timezone.now()
        super(Articles, self).save(*args, **kwargs)
    @property
    def countview(self):
        c = 0
        for i in ArticleViewCount.objects.filter(article_instance = self):
            c += i.count

        return c

class ArticleViewCount(models.Model):
    article_instance = models.ForeignKey(Articles, related_name='view_count', on_delete=models.CASCADE)
    user = models.ManyToManyField(User, related_name="articleviewuser")
    count = models.IntegerField(blank=True, null=True, default=0)
    created = models.DateField(blank=True, default=date.today)
    def __str__(self):
        return self.article_instance.title
    

class BlogComment(models.Model):
    user = models.ForeignKey(User, related_name='blog_comment_user', to_field='username', on_delete=models.CASCADE,default="")
    question = models.ForeignKey(Articles, related_name='blog_comment_ques',on_delete=models.CASCADE,default="")
   
    parent = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE,related_name="replies_name")
    body = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True,null=True)
    active = models.BooleanField(default=True)
    like = models.ManyToManyField(User,related_name="blog_comment_like")
    dislike = models.ManyToManyField(User,related_name="blog_comment_dislike")
    class Meta:
        ordering = ('-created',)
    def children(self):
        return BlogComment.objects.filter(parent=self).order_by("id")

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
    @property
    def sorting(self):
        return BlogComment.objects.filter(parent = self).order_by("created")
    def __str__(self):
        return self.body

