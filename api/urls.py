from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.profile_list, name='profile-list'),
    path('predict/', views.predict_anomaly, name='predict-anomaly'),
]
