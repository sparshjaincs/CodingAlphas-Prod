from django.urls import path
from . import views
urlpatterns = [
    path("",views.homepage,name="blog_page"),
    path("save/",views.save,name="save"),
    path("create/new/",views.create,name="create"),
    path("<id>/edit/",views.edit,name="edit"),
    path("preview/fetch/",views.preview_data,name="preview_data"),
    path("submit/post/",views.post,name="post"),
    path("read/<user>/<title>/<id>/",views.mainpage,name="mainpage"),
    path("comment/post/",views.comment,name="comment"),
    path("upload/body/",views.image_upload, name="image_upload"),
    path("analytics/data/fetch/",views.analytics_data,name="analytics_data"),
    path("analytics/data/fetch/all/",views.analytics_dataall,name="analytics_dataall"),
]