from django.urls import path
from . import views

urlpatterns = [
	path('', views.index),
	path('login/', views.login),
	path('signup/', views.signup),
	path('logout/', views.logout),
	path('newgroup/', views.newgroup),
	path('mygroups/<int:group_id>/',views.groupMembers),
	path('mygroups/',views.mygroups),
	path('searchforadding/<grpid>/<searchKey>', views.searchforadding),
	path('addusertogrp/<grpid>/<userid>/', views.addusertogrp),
	path('removeuserfrmgrp/<grpid>/<userid>/', views.removeuserfrmgrp),
	path('delgrp/<grpid>/', views.delgrp),
	path('addbill/', views.showallgrps),
	path('addbill/<grpid>/', views.addbill),
	path('settlerequest/<transactionId>/', views.settlerequest),
	path('settle/<requestId>/<transactionId>/', views.settle)
]