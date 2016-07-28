from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


from .models import tour_user, Tour , stops#relative import



class tour_user_Inline(admin.StackedInline):
    model = tour_user
    can_delete = False
    verbose_name_plural = 'tour_user'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (tour_user_Inline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here.

# class tour_user_Admin(admin.ModelAdmin):
#     class Meta:
#         model = tour_user

class TOUR_Admin(admin.ModelAdmin):
    class Meta:
        model = Tour
class Stops_Admin(admin.ModelAdmin):
    class Meta:
        model = stops

# admin.site.register(tour_user, tour_user_Admin)
admin.site.register(Tour, TOUR_Admin)
admin.site.register(stops, Stops_Admin)