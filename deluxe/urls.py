from django.contrib import admin
from django.urls import path
from reservation import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('booking', views.booking),
    path('rooms', views.rooms),
    path('room<int:r_no>', views.each_room),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('reservations-chart', views.reservations),
    path('logins-chart', views.logins),
    path('logout', views.logout),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
