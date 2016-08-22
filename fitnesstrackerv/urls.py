from django.conf.urls import url, patterns
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	url(r'^$', views.goal_list, name='goal_list'),
	url(r'^goal/new/$', views.new_goal, name='new_goal'),
	url(r'^goal/update/(?P<pk>\d+)/$', views.update_progress, name='update_progress'),
	url(r'^goal/(?P<pk>\d+)/$', views.goal_detail, name='goal_detail'),
	url(r'^deletegoal/(?P<pk>\d+)/$', views.delete_goal, name='delete_goal'),
	url(r'^api/$', views.api_list),
	url(r'^api/(?P<pk>[0-9]+)/$', views.api_detail),
	url(r'^login/$', auth_views.login, name='login'),
	url(r'^logout/$', auth_views.logout, name='logout'),
]
urlpatterns = format_suffix_patterns(urlpatterns)