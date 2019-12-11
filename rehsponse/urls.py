from django.urls import path, include, re_path
from rehsponse import views


urlpatterns = [
    path('api/', include('rehsponse.api.urls')),  # /api/
    path('login/', views.AuthView.as_view(), name="auth_page"),  # /login
    path('search/', views.RehsponseListView.as_view(), name="list"),  # /search
    path('rehsponse/<int:pk>/', views.RehsponseDetailView.as_view(), name="detail"),  # /rehsponse/1
    path('rehsponse/create/', views.RehsponseCreateView.as_view(), name="create"),  # /rehsponse/create
    path('rehsponse/<int:pk>/edit', views.RehsponseUpdateView.as_view(), name="update"),  # /rehsponse/1/edit
    path('rehsponse/<int:pk>/delete', views.RehsponseDeleteView.as_view(), name="delete")  # /rehsponse/1/delete
]
