from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    
    path('',views.index,name='Home'),
    path('about/',views.about,name='about'),
    path('trainers/',views.trainers,name='trainers'),
    path('membership/',views.membership,name='membership'),
    path('contact/',views.contact,name='contact'),
     path('signup/',views.signupp,name='signup'),
      path('login/',views.loginn,name='login'),
     
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
