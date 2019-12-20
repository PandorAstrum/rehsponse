from django.urls import path, include, re_path
from django.contrib.sitemaps.views import sitemap
from rehsponse import views
from rehsponse.sitemaps import RehsponseSitemap

sitemaps = {
    'rehsponse' : RehsponseSitemap,
}

urlpatterns = [
    path('api/', include('rehsponse.api.urls')),  # /api/
    path('login/', views.AuthView.as_view(), name="auth_page"),  # /login
    path('search/', views.RehsponseListView.as_view(), name="list"),  # /search

    path('rehsponse/<int:pk>/', views.RehsponseDetailView.as_view(), name="detail"),  # /rehsponse/1
    path('rehsponse/<int:pk>/reply', views.RehsponseReplyView.as_view(), name="reply"),  # /rehsponse/1/reply
    path('rehsponse/create/', views.RehsponseCreateView.as_view(), name="create"),  # /rehsponse/create
    path('rehsponse/<int:pk>/edit', views.RehsponseUpdateView.as_view(), name="update"),  # /rehsponse/1/edit
    path('rehsponse/<int:pk>/delete', views.RehsponseDeleteView.as_view(), name="delete"),  # /rehsponse/1/delete

    re_path(r'^user/(?P<username>\w+)/rehsponses$', views.UserDetailView.as_view(), name='userdetail'),  # /user/username/rehsponses
    re_path(r'^user/(?P<username>\w+)/edit$', views.UserUpdateView.as_view(), name='useredit'),  # /user/username/edit

    re_path(r'^tags/(?P<hashtag>.*)/$', views.HashTagView.as_view(), name='hashtag'),  # /tag/hashtag
    path('contacts/', views.ContactListView.as_view(), name="contact"),  # /contacts/
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name="sitemaps"),

    # path('user/<slug:first_name>/', views.UserDetailView.as_view(), name="userdetail"),
    # path('rehsponse/create/', views.RehsponseCreateView.as_view(), name="create"),  # /rehsponse/create
    # path('rehsponse/<int:pk>/edit', views.RehsponseUpdateView.as_view(), name="update"),  # /rehsponse/1/edit
    # path('rehsponse/<int:pk>/delete', views.RehsponseDeleteView.as_view(), name="delete")  # /rehsponse/1/delete
]
