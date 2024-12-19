from django.urls import path

from .views import (
    add_user,
    edit_user,
    users_list,
    get_user,
    login,

    attendance_list,
    edit_attendance,

    etiquette_list,
    edit_etiquette,
)


urlpatterns = [
    # auth
    path("auth/login/", login, name="login"),

    # admin.users
    path("admin/users/edit/<str:uuid>/", edit_user, name="edit_user"),
    path("admin/users/add/", add_user, name="add_user"),
    path("admin/users/", users_list, name="users"),
    path("admin/users/user/<str:uuid>/", get_user, name="get_user"),

    path("admin/attendances/", attendance_list, name="attendance_list"),
    path("admin/attendances/edit/", edit_attendance, name="edit/attendance"),

    path("admin/etiquettes/", etiquette_list, name="etiquette_list"),
    path("admin/etiquettes/edit/", edit_etiquette, name="edit_etiquette"),
]
