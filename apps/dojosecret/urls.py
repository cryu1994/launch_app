from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^success/(?P<sort>\w+)$', views.success),
    url(r'^create_comment$', views.create_comment),
    url(r'^delete/(?P<comment_id>\d+)', views.delete_comment),
    url(r'^like/(?P<comment_id>\d+)', views.like),
    url(r'^unlike/(?P<comment_id>\d+)', views.unlike),
]
