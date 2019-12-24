from django.urls import path
from rehsponse.api import views

urlpatterns = [
    path('login/', views.UserLoginApiView.as_view()),
    path('list/', views.RehsponseListAPIView.as_view(), name='apilist'),                    # api/list api/list/?q=bla (search)
    path('rehsponse/<int:pk>/', views.RehsponseDetailAPIView.as_view(), name="apidetail"),  # api/rehsponse/1
    path('rehsponse/create/', views.RehsponseCreateAPIView.as_view(), name="apicreate"),    # api/rehsponse/create
    path('rehsponse/<int:pk>/edit', views.RehsponseUpdateAPIView.as_view(), name="apiupdate"),  # api/rehsponse/1/edit
    path('rehsponse/<int:pk>/delete', views.RehsponseDeleteAPIView.as_view(), name="apidelete"),  # api/rehsponse/1/delete
    path('rehsponse/<int:pk>/loved/', views.LoveToggleAPIView.as_view(), name="apilove"),   # api/rehsponse/1/loved

    path('tags/', views.HashTagListAPIView.as_view(), name="apitags"),                      # api/tags
    path('contacts/', views.ContactListAPIView.as_view(), name="apicontact"),               # api/contacts

    path('user/create/', views.UserCreateAPIView.as_view(), name="apiusercreate"),          # api/user/create
    path('user/<str:username>/rehsponses', views.UserDetailAPIView.as_view(), name="apiuserdetail"),  # api/user/123/rehsponses
    path('user/<str:username>/edit', views.RehsponseUpdateAPIView.as_view(), name="apiuserupdate"),  # api/user/123/edit
    path('user/<str:username>/delete', views.RehsponseDeleteAPIView.as_view(), name="apiuserdelete"),  # api/user/123/delete
]