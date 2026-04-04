from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    
    path('',views.index,name='Index'),
     path('Home/',views.Home,name='Home'),
     path('Logout/',views.logout,name='Logout'),
    path('about/',views.about,name='about'),
    path('trainers/',views.trainners,name='trainers'),
    path('membership/',views.memberships,name='membership'),
    path('contact/',views.contact,name='contact'),
     path('signup/',views.signupp,name='signup'),
      path('login/',views.loginn,name='login'),
     path('profile',views.profile,name='profile'),
     path('classes',views.classes,name='classes'),
      path('payment/<str:method>/', views.payment_view, name='payment'),
    path('payment-success/', views.payment_success_view, name='payment_success'),
    path("booked/", views.bookedclass, name="bookedclass"),
    path('attendance-mark/',views.attendance_mark, name='attendance_mark'),
    path('trainer/login/',views.trainer_login_view,name="trainerlogin"),
    path('unapproved/', views.unapproved_trainer, name='unapproved_trainer'),
    path('update/', views.update, name='update'),
    path('expired_memberships/', views.expired_memberships_view, name='expired_memberships'),
    path('book-class/', views.book_class_view, name='book_class'),
     path('select/', views.select_date_time, name='select_date_time'),
     path('trainer/class-bookings/', views.trainer_class_bookings, name='trainer_class_bookings'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
