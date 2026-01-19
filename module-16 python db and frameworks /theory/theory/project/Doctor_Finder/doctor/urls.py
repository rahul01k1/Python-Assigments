from django.urls import path
from . import views

app_name = 'doctor'

urlpatterns = [
    path('', views.home, name='home'),
     path("services/", views.services_page, name="services"),
    path("contact/", views.contact_page, name="contact"),
    path("about/", views.about_page, name="about"),
    path("doctors/", views.doctor_list, name="doctor_list"),
    path("doctors/<int:id>/", views.doctor_detail, name="doctor_detail"),
    path("doctor/<int:doctor_id>/", views.doctor_profile, name="doctor_profile"),
    path("doctor/dashboard/", views.doctor_dashboard, name="doctor_dashboard"),


    path("book-appointment/<int:doctor_id>/", views.book_appointment, name="book_appointment"),
    path("appointment/approve/<int:appointment_id>/", views.approve_appointment, name="approve_appointment"),
    path("appointment/reject/<int:appointment_id>/", views.reject_appointment, name="reject_appointment"),

    path("patient/dashboard/", views.patient_dashboard, name="patient_dashboard"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.profile_update, name="profile_update"),
    path("my-appointments/",views.my_appointments,name="my_appointments"),

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]
