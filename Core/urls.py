from django.urls import path
from . import views
urlpatterns = [
    path("",views.homepage,name="homepage"),
    path("profile/<user>/",views.profile,name="profile"),
    
     path("signingup/",views.signingup,name="signingup"),
    path("profile/settings/data/save/",views.profiledata, name="profiledata"),
     path("profile/<user>/",views.profile,name="profile"),
     path("photo/upload/list/",views.photo_upload,name="photo_upload"),
     path("video/upload/list/",views.video_upload,name="video_upload"),
     path("post/upload/list/",views.post_upload,name="post_upload"),
     path("settings/",views.settings,name="settings"),
     path("notification_balance/", views.notification_balance,name="notification_balance"),
     path("activities/<method>/<value>/",views.activities,name="activities"),
    path("delete/all/",views.delete,name="delete"),
     path("news/<topic>/",views.news,name="news"),
     path("news/ajax/fetch",views.ajax_news,name="ajax_news"),
     path("coming_soon/",views.coming_soon,name="comming_soon"),
      path("like/",views.like,name="like"),
     path("dislike/",views.dislike,name="dislike"),
     path("follow/",views.follow,name="follow"),
     path("mark/",views.mark,name="mark"),
     path("comment_submit/", views.comment_submit, name="comment_submit"),
   
]