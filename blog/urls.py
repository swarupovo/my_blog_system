from django.conf.urls import url
from blog import views
urlpatterns = [    # post views
    url(r'^$', views.BlogList.as_view(), name='post_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', views.post_detail, name='post_detail'),
    url(r'^blog/post/$', views.post_form, name="post_blog")
]