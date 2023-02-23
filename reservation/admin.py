from django.contrib import admin
from .models import *

admin.site.register(Room)
admin.site.register(Guest)
admin.site.register(Reservation)
admin.site.register(Service)
admin.site.register(Payment)
admin.site.register(LoginStat)