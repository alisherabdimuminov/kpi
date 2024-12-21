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

    tasks_list,
    add_task,
    delete_task,
    user_tasks_list,

    submits_list,
    change_submit_status,
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

    path("admin/tasks/", tasks_list, name="tasks_list"),
    path("admin/tasks/add/", add_task, name="add_task"),
    path("admin/tasks/delete/", delete_task, name="delete_task"),
    path("user/tasks/", user_tasks_list, name="user_tasks_list"),

    path("admin/submits/", submits_list, name="submits_list"),
    path("admin/submits/change/", change_submit_status, name="change_submit_status"),
]
