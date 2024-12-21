from datetime import datetime, timedelta
from django.http import HttpRequest
from rest_framework import decorators
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import (
    Application,
    Attendance,
    Etiquette,
    Submit,
    Task,
    User,
    Rate,
)

from .serializers import (
    ApplicationGETSerializer,
    AttendanceGETSerializer,
    EtiquetteGETSerializer,
    SubmitGETSerializer,
    UserADDSerializer,
    UserGETSerializer,
    TaskGETSerializer,
    TaskADDSerializer,
)


# ===== AUTHENTICATION AND AUTHORIZATION =====
# ===== LOGIN HANDLER FOR ALL USERS =====
@decorators.api_view(http_method_names=["POST"])
def login(request: HttpRequest):
    username = request.data.get("username", None)
    password = request.data.get("password", None)

    if username != None and password != None:
        user = User.objects.filter(username=username)
        if user:
            user = user.first()
            check_password = user.check_password(password)
            if check_password:
                image = user.image
                if image:
                    image = request.build_absolute_uri(image.url)
                else:
                    image = None
                token = Token.objects.get_or_create(user=user)
                data = {
                    "uuid": user.uuid,
                    "username": user.username,
                    "full_name": user.full_name,
                    "image": image,
                    "passport_number": user.passport_number,
                    "passport_pinfl": user.passport_pinfl,
                    "branch": user.branch,
                    "department": user.department,
                    "position": user.position,
                    "role": user.role,
                    "token": token[0].key,
                }
                return Response({
                    "status": "success",
                    "code": "",
                    "data": data
                })
            else:
                return Response({
                    "status": "error",
                    "code": "001",
                    "data": None
                })
        else:
            return Response({
                "status": "error",
                "code": "002",
                "data": None
            })
    else:
        return Response({
            "status": "error",
            "code": "003",
            "data": None
        })


# ===== ADD USER FOR ONLY ADMIN =====
@decorators.api_view(http_method_names=["POST"])
def add_user(request: HttpRequest):
    data = request.data.copy()
    password = data.pop("password")[0]
    serializer = UserADDSerializer(data=data)

    if serializer.is_valid():
        user = serializer.save()
        user.set_password(password)
        user.save()
        return Response({
            "status": "success",
            "code": "",
            "data": None
        })
    else:
        errors = serializer.errors.keys()
        print(errors)
        return Response({
            "status": "error",
            "code": "",
            "data": {
                "errors": errors
            }
        })


# ===== EDIT USER FOR ONLY ADMIN =====
@decorators.api_view(http_method_names=["POST"])
def edit_user(request: HttpRequest, uuid: str):
    data = request.data.copy()
    user = User.objects.get(uuid=uuid)
    serializer = UserADDSerializer(user, data=data)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "code": "200",
            "data": None
        })
    else:
        print(data)
        errors = serializer.errors.keys()
        print(serializer.error_messages)
        print(serializer.errors)
        return Response({
            "status": "error",
            "code": "400",
            "data": {
                "errors": errors
            }
        })


# ===== USERS LIST FOR ONLY ADMIN =====
@decorators.api_view(http_method_names=["GET"])
def users_list(request: HttpRequest):
    branch = request.GET.get("branch")
    department = request.GET.get("department")
    users_obj = User.objects.all().order_by("full_name").exclude(role="admin")

    if branch and branch != "0":
        users_obj = users_obj.filter(branch=branch).order_by("full_name")
    if department and department != "0":
        users_obj = users_obj.filter(department=department)
    users = UserGETSerializer(users_obj, many=True)
    return Response({
        "status": "success",
        "code": "200",
        "data": users.data
    })


# ===== USER GET FOR ONLY ADMIN
@decorators.api_view(http_method_names=["GET"])
def get_user(request: HttpRequest, uuid: str):
    user_obj = User.objects.get(uuid=uuid)
    user = UserGETSerializer(user_obj, many=False)
    return Response({
        "status": "success",
        "code": "200",
        "data": user.data
    })


# ===== ATTENDANCE =====
# ===== ATTENDANCE LIST FOR ONLY ADMIN =====
@decorators.api_view(http_method_names=["GET"])
def attendance_list(request: HttpRequest):
    current_date = datetime.now()
    week_ago = (current_date - timedelta(days=7)) 
    start_day = request.GET.get("start_day", week_ago.day)
    start_month = request.GET.get("start_month", week_ago.month)
    start_year = request.GET.get("start_year", week_ago.year)
    end_day = request.GET.get("end_day", current_date.day)
    end_month = request.GET.get("end_month", current_date.month)
    end_year = request.GET.get("end_year", current_date.year)
    branch = request.GET.get("branch")
    department = request.GET.get("department")

    users = User.objects.all().order_by("full_name").exclude(role="admin")

    if branch and branch != "0":
        users = users.filter(branch=branch).order_by("full_name")
    if department and department != "0":
        users = users.filter(department=department).order_by("full_name")

    start_date = datetime.strptime(f"{start_day}/{start_month}/{start_year}", "%d/%m/%Y")
    end_date = datetime.strptime(f"{end_day}/{end_month}/{end_year}", "%d/%m/%Y")

    date_range = [(start_date + timedelta(days=i)).strftime("%d-%m-%Y") for i in range((end_date - start_date).days + 1)]

    attendances = {}

    for date in date_range:
        day, month, year = date.split("-")
        attendance = AttendanceGETSerializer(users, many=True, context={ "date": { "day": day, "month": month, "year": year } })
        attendances[date] = attendance.data
    
    return Response({
        "status": "success",
        "code": "200",
        "data": attendances
    })


# ===== ATTENDANCE EDIT FOR ONLY ADMIN =====
@decorators.api_view(http_method_names=["POST"])
def edit_attendance(request: HttpRequest):
    user_uuid = request.data.get("uuid")
    date = request.data.get("date")
    date = datetime.strptime(date, "%d-%m-%Y")
    attendance = Attendance.objects.filter(user__uuid=user_uuid, created=date).first()
    attendance.is_arrived = not attendance.is_arrived
    attendance.save()
    return Response({
        "status": "success",
        "code": "200",
        "data": None,
    })


# ===== ETIQUETTE
# ===== ETIQUETTE LIST FOR ONLY ADMIN =====
@decorators.api_view(http_method_names=["GET"])
def etiquette_list(request: HttpRequest):
    months = {
        1: "Yanvar", 
        2: "Fevral", 
        3: "Mart", 
        4: "Aprel", 
        5: "May", 
        6: "Iyun", 
        7: "Iyul", 
        8: "Avgust", 
        9: "Sentabr", 
        10: "Oktabr", 
        11: "Noyabr", 
        12: "Dekabr",
    }
    now = datetime.now()
    month = now.month
    year = now.year
    branch = request.GET.get("branch")
    department = request.GET.get("department")

    users = User.objects.all().order_by("full_name").exclude(role="admin")

    if branch and branch != "0":
        users = users.filter(branch=branch).order_by("full_name")
    if department and department != "0":
        users = users.filter(department=department).order_by("full_name")

    etiquettes = {}

    for m in range(1, 12 - (12 - month) + 1):
        etiquette = EtiquetteGETSerializer(users, many=True, context={ "date": { "month": m, "year": year } })
        etiquettes[months[m]] = etiquette.data
    
    return Response({
        "status": "success",
        "code": "200",
        "data": etiquettes
    })


# ===== ETIQUETTE EDIT FOR ONLY ADMIN =====
@decorators.api_view(http_method_names=["POST"])
def edit_etiquette(request: HttpRequest):
    months = {
        "Yanvar": 1, 
        "Fevral": 2, 
        "Mart": 3, 
        "Aprel": 4, 
        "May": 5, 
        "Iyun": 6, 
        "Iyul": 7, 
        "Avgust": 8, 
        "Sentabr": 9, 
        "Oktabr": 10, 
        "Noyabr": 11, 
        "Dekabr": 12,
    }
    now = datetime.now()
    user_uuid = request.data.get("uuid")
    month = months.get(request.data.get("month"))
    year = now.year
    point = request.data.get("point")
    etiquette = Etiquette.objects.filter(user__uuid=user_uuid, created__month=month, created__year=year).first()
    etiquette.point = point
    etiquette.save()
    return Response({
        "status": "success",
        "code": "200",
        "data": None,
    })


# ===== TASK =====
# ===== TASKS FOR ONYLY ADMINS =====
@decorators.api_view(http_method_names=["GET"])
def tasks_list(request: HttpRequest):
    tasks_obj = Task.objects.all()
    tasks = TaskGETSerializer(tasks_obj, many=True)
    return Response({
        "status": "success",
        "code": "200",
        "data": tasks.data
    })


# ===== ADD TASK FOR ONLY ADMINS =====
@decorators.api_view(http_method_names=["POST"])
def add_task(request: HttpRequest):
    serializer = TaskADDSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "code": "200",
            "data": None
        })
    else:
        errors = serializer.error_messages
        print(serializer.errors)
        return Response({
            "status": "error",
            "code": "400",
            "data": {
                "errors": errors
            }
        })


# ===== DELETE TASK FOR ONLY ADMINS =====
@decorators.api_view(http_method_names=["POST"])
def delete_task(request: HttpRequest):
    task_uuid = request.data.get("uuid")
    task = Task.objects.get(uuid=task_uuid)
    task.delete()
    return Response({
        "status": "success",
        "code": "200",
        "data": None
    })


# ===== TASKS FOR ONYLY EMPLOYEES =====
@decorators.api_view(http_method_names=["GET"])
def user_tasks_list(request: HttpRequest):
    user = request.user
    tasks_obj = Task.objects.filter(position=user.position)
    tasks = TaskGETSerializer(tasks_obj, many=True)
    return Response({
        "status": "success",
        "code": "200",
        "data": tasks.data
    })


# ===== SUBMITS =====
# ===== SUBMITS FOR ONLY ADMIN =====
@decorators.api_view(http_method_names=["GET"])
def submits_list(request: HttpRequest):
    submits_obj = Submit.objects.all()
    submits = SubmitGETSerializer(submits_obj, many=True)
    return Response({
        "status": "success",
        "code": "200",
        "data": submits.data
    })

# ===== CHANGE SUBMITS STATUS FOR ONLY ADMINS =====
@decorators.api_view(http_method_names=["POST"])
def change_submit_status(request: HttpRequest):
    now = datetime.now()
    submit_uuid = request.data.get("uuid")
    status = request.data.get("status")
    submit = Submit.objects.get(uuid=submit_uuid)
    submit.status = status
    submit.save()
    if submit.status == "approved":
        rate = Rate.objects.filter(created__month=now.month, created__year=now.year, user_id=submit.user.pk, )
        if rate:
            rate = rate.first()
            rate.point = rate.point + submit.task.point
            rate.save()
        else:
            rate = Rate.objects.create(user=submit.user, point=0, created=now)
            rate.point = rate.point + submit.task.point
            rate.save()
    return Response({
        "status": "success",
        "code": "201",
        "data": None
    })
