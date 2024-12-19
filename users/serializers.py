from datetime import datetime

from rest_framework import serializers

from .models import (
    Application,
    Attendance,
    Etiquette,
    Submit,
    Task,
    User,
)


class ApplicationGETSerializer(serializers.ModelSerializer):
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


