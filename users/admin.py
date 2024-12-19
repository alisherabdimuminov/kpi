from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import (
    Application,
    Attendance,
    Etiquette,
    Submit,
    Task,
    User,
)


@admin.register(Application)
class ApplicationModelAdmin(admin.ModelAdmin):
    list_display = ["number", "status", "created", ]


@admin.register(Attendance)
class AttendanceModelAdmin(admin.ModelAdmin):
    list_display = ["user", "is_arrived", "created"]


@admin.register(Etiquette)
class EtiquetteModelAdmin(admin.ModelAdmin):
    list_display = ["user", "point", "created"]


@admin.register(Submit)
class SubmitModelAdmin(admin.ModelAdmin):
    list_display = ["user", "task", "status", ]


@admin.register(Task)
class TaskModelAdmin(admin.ModelAdmin):
    list_display = ["name", "point", "term", ]


@admin.register(User)
class UserModelAdmin(UserAdmin):
    list_display = ["uuid", "username", "full_name", ]
    add_form = UserCreationForm
    form = UserChangeForm
    add_fieldsets = (
        ("Yangi foydalanuvchi qo'shish", {
            "fields": ("username", "password1", "password2", "full_name", "role", )
        }),
    )
    fieldsets = (
        ("Foydalanuvchini tahrirlash", {
            "fields": ("uuid", "username", "full_name", "role", "image", )
        }),
        ("Xodim malumotlari", {
            "fields": ("branch", "department", "position", "passport_number", "passport_pinfl", )
        }),
    )
