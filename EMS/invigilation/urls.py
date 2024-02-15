from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.homePage, name='home'),
    path('user-login', views.userlogin, name='login'),
    path('logout', views.userlogout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('halls', views.halls, name='halls'),
    # path('departments', views.departments, name='departments'),
    path('lecturers', views.lecturers, name='lecturers'),
    path('schedule', views.schedule, name='schedule'),
    # path('Upload-departments', views.upload_department, name='upload_department'),
    path('Upload-halls', views.upload_hall, name='upload_hall'),
    path('Upload-lecturers', views.upload_lecturers, name='upload_lecturers'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
