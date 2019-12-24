from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from rehsponse import views
from rehsponse.sitemaps import RehsponseSitemap

sitemaps = {
    'rehsponse' : RehsponseSitemap,
}

urlpatterns = [
    path('api/', include('rehsponse.api.urls')),  # /api/
    path('login/', views.UserLoginView.as_view(), name="login"),  # /login
    path('logout/', views.logout_view, name="logout"),  # /logout
    path('signup/', views.UserRegistrationView.as_view(), name="signup"),  # /logout
    path('password_reset/', views.UserLoginView.as_view(), name="password_reset"),  # /login
    path('search/', views.RehsponseListView.as_view(), name="list"),  # /search

    path('rehsponse/<int:pk>/', views.RehsponseDetailView.as_view(), name="detail"),  # /rehsponse/1
    path('rehsponse/create/', views.RehsponseCreateView.as_view(), name="create"),
    path('rehsponse/board/', views.RehsponseBoardListView.as_view(), name="board"),

    re_path(r'^user/(?P<user_name>\w+)/rehsponses$', views.UserDetailView.as_view(), name='userdetail'),  # /user/username/rehsponses
    re_path(r'^user/(?P<user_name>\w+)/edit$', views.UserUpdateView.as_view(), name='useredit'),  # /user/username/edit

    re_path(r'^tags/(?P<hashtag>.*)/$', views.HashTagView.as_view(), name='hashtag'),  # /tag/hashtag
    path('contacts/', views.ContactListView.as_view(), name="contact"),  # /contacts/
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name="sitemaps"),
]
