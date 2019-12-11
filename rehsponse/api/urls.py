from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rehsponse.api import views

router = DefaultRouter()
router.register('user', views.UserProfileViewSets)
router.register('post', views.PostViewSets)

urlpatterns = [
    path('login/', views.UserLoginApiView.as_view()),
    path('', include(router.urls)),
    path('list/', views.RehsponseListView.as_view(), name='apilist'),  # api/list
]