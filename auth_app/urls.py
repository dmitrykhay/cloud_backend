from django.urls import path
from .views import UserView
from auth_app.registration import registration
from auth_app.log_in import log_in    

urlpatterns = [
    path('registration/', registration),
    path('log_in/<str:username>/<str:password>/',log_in),
]