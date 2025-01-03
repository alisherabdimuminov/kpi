from datetime import datetime

from rest_framework import serializers

from .models import (
    Application,
    Attendance,
    Etiquette,
    Rate,
    Submit,
    Task,
    User,
)


class ApplicationGETSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    class Meta:
        model = Application
        fields = ('uuid', 'number', 'file', 'status', 'created', 'updated', )


class AttendanceGETSerializer(serializers.ModelSerializer):
    requires_context = True

    is_arrived = serializers.SerializerMethodField("is_arrived_func")

    def is_arrived_func(self, obj: User):
        now = datetime.now()
        date = self.context.get("date")
        day = date.get("day", now.day)
        month = date.get("month", now.month)
        year = date.get("year", now.year)
        date = datetime.strptime(f"{day}-{month}-{year}", "%d-%m-%Y")
        attendance = Attendance.objects.filter(user_id=obj.pk, created__day=day, created__month=month, created__year=year)
        if attendance:
            attendance = attendance.first()
            return attendance.is_arrived
        else:
            print(attendance)
            attendance = Attendance.objects.create(user=obj, is_arrived=True, created=date)
            return attendance.is_arrived

    class Meta:
        model = User
        fields = ('uuid', 'username', 'full_name', 'branch', 'department', 'position', 'is_arrived', )


class EtiquetteGETSerializer(serializers.ModelSerializer):
    requies_context = True

    point = serializers.SerializerMethodField('point_func')

    def point_func(self, obj: User):
        now = datetime.now()
        date = self.context.get("date")
        month = date.get("month", now.month) 
        year = date.get("year", now.year)
        created = datetime.strptime(f"01-{month}-{year}", "%d-%m-%Y")
        etiquette = Etiquette.objects.filter(user_id=obj.pk, created__month=month, created__year=year)
        print(etiquette)
        if etiquette:
            etiquette = etiquette.first()
            return etiquette.point
        else:
            etiquette = Etiquette.objects.create(user=obj, point="3", created=created)
            return etiquette.point

    class Meta:
        model = User
        fields = ('uuid', 'username', 'full_name', 'branch', 'department', 'position', 'point', )


class UserGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uuid', 'pid', 'username', 'full_name', 'image', 'passport_number', 'passport_pinfl', 'branch', 'department', 'position', 'role', )


class UserADDSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_null=True, required=False)
    class Meta:
        model = User
        fields = ('uuid', 'username', 'pid', 'full_name', 'image', 'passport_number', 'passport_pinfl', 'branch', 'department', 'position', 'role', )


class RateGETSerializer(serializers.ModelSerializer):
    user = UserGETSerializer(User, many=False)
    class Meta:
        model = Rate
        fields = ("user", "point", )

class TaskGETSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    class Meta:
        model = Task
        fields = ("uuid", "name", "point", "term", "position", "created", )


class TaskADDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("name", "point", "term", "position", )


class SubmitGETSerializer(serializers.ModelSerializer):
    user = UserGETSerializer(User, many=False)
    task = TaskGETSerializer(Task, many=False)
    created = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    class Meta:
        model = Submit
        fields = ("uuid", "user", "task", "file", "status", "created")

class TaskWSGETSerializer(serializers.ModelSerializer):
    requies_context = True

    created = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    status = serializers.SerializerMethodField("status_func")

    def status_func(self, obj: Task):
        request = self.context.get("request")
        submit = Submit.objects.filter(user_id=request.user.pk, task_id=obj.pk)
        if submit:
            submit = submit.last()
            return submit.status
        else:
            return "given"

    class Meta:
        model = Task
        fields = ("uuid", "name", "point", "term", "position", "created", "status", )