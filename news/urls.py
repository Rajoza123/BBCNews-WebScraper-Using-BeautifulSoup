from django.urls import path
from news import views

urlpatterns = [
    path("",views.homepage,name='home'),
    path('sports/',views.scrape_sports,name='sport'),
    path('enter/',views.scrape_entertainment,name='entertain'),
    path('business/',views.scrape_business,name='business')
]
