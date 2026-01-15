from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page, name='landing'),
    path('dashboard/', views.home, name='home'),
    path('about/', views.about_us, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/whatsapp/', views.contact_whatsapp, name='contact_whatsapp'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('note/<int:note_id>/', views.note_detail, name='note_detail'),
    path('note/<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('create/', views.create_note, name='create_note'),
]