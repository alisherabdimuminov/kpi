from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager


TERM = (
    ("regular", "Doimiy"),
    ("monthly", "Oylik"),
    ("quarter", "Chorak"),
    ("annual", "Yillik"),
)
ROLE = (
    ("admin", "Admin"),
    ("analyst", "Mutaxasis axborot tahlil"),
    ("cadre", "Mutaxasis kadr"),
    ("user", "Xodim"),
    ("userx", "XodimX"),
)
STATUS = (
    ("approved", "Tasdiqlangan"),
    ("rejected", "Rad etilgan"),
    ("in_process", "Jarayonda"),
    ("created", "Yaratilgan"),
)
BRANCH = (
    ("Davlat ekologik ekspertiza markazi", "Davlat ekologik ekspertiza markazi"),
    ("Qoraqalpog'iston respublikasi filiali", "Qoraqalpog'iston respublikasi filiali"),
    ("Andijon viloyati filiali", "Andijon viloyati filiali"),
    ("Buxoro viloyati filiali", "Buxoro viloyati filiali", ),
    ("Farg'ona viloyati filiali", "Farg'ona viloyati filiali"),
    ("Jizzax viloyati filiali", "Jizzax viloyati filiali", ),
    ("Qashqadaryo viloyati filiali", "Qashqadaryo viloyati filiali", ),
    ("Navoi viloyati filiali", "Navoi viloyati filiali", ),
    ("Namangan viloyati filiali", "Namangan viloyati filiali", ),
    ("Samarqand viloyati filiali", "Samarqand viloyati filiali", ),
    ("Surxondaryo viloyati filiali", "Surxondaryo viloyati filiali", ),
    ("Sirdaryo viloyati filiali", "Sirdaryo viloyati filiali", ),
    ("Toshkent viloyati filiali", "Toshkent viloyati filiali", ),
    ("Toshkent shahri filiali", "Toshkent shahri filiali", ),
    ("Xorazm viloyati filiali", "Xorazm viloyati filiali", ),
)
DEPARTMENT = (
    ("Raxbariyat", "Raxbariyat",),
    ("Ichki nazorat xizmati", "Ichki nazorat xizmati",),
    ("Yuridik xizmati", "Yuridik xizmati",),
    ("Buxgalteriya bo'limi", "Buxgalteriya bo'limi"),
    ("Birinchi bo'lim", "Birinchi bo'lim",),
    ("Inson resurslarini boshqarish", "Inson resurslarini boshqarish",),
    ("Davlat tiliga rioya etilishini ta'minlash masalari", "Davlat tiliga rioya etilishini ta'minlash masalari",),
    ("Xo'jalik ishlari bo'limi", "Xo'jalik ishlari bo'limi",),
    ("Metodologiya bo'limi", "Metodologiya bo'limi",),
    ("Xalqaro konvensiyalar bilan ishlash bo'limi", "Xalqaro konvensiyalar bilan ishlash bo'limi",),
    ("Ijro intizomi bo'limi", "Ijro intizomi bo'limi",),
    ("Axborot kommunikatsiya texnologiyalarini rivojlantirish", "Axborot kommunikatsiya texnologiyalarini rivojlantirish",),
    ("Jamoatchilik bilan ishlash bo'limi", "Jamoatchilik bilan ishlash bo'limi",),
    ("Davlat ekologik ekpertizasini o'tkazish boshqarmasi", "Davlat ekologik ekpertizasini o'tkazish boshqarmasi",),
    ("Davlat ekologik ekspertizasiga arizalarni qabul qilish bo'limi", "Davlat ekologik ekspertizasiga arizalarni qabul qilish bo'limi",),
    ("Ekologik ekspertiza obyektlarini to'yobga chiqarish bo'limi", "Ekologik ekspertiza obyektlarini to'yobga chiqarish bo'limi",),
    ("Axborot tahlil bo'limi", "Axborot tahlil bo'limi",),
    ("Monitoring bo'limi", "Monitoring bo'limi",),
    ("Texnik va xizmat ko'rsatish xodimlari", "Texnik va xizmat ko'rsatish xodimlari",),
)
POSITION = (
    ("Bosh direktor", "Bosh direktor",),
    ("Bosh direktorning birinchi o'rinbosari", "Bosh direktorning birinchi o'rinbosari",),
    ("Bosh direktor o'ribosari", "Bosh direktor o'ribosari",),
    ("Bosh direktor maslahatchisi", "Bosh direktor maslahatchisi", ),
    ("Bosh yuriskonsult", "Bosh yuriskonsult", ),
    ("Bo'lim boshlig'i", "Bo'lim boshlig'i", ),
    ("Bosh mutaxasis", "Bosh mutaxasis", ),
    ("Yetakchi mutaxasis", "Yetakchi mutaxasis", ),
    ("Texnik xodim", "Texnik xodim", ),
    ("Filial direktori", "Filial direktori", ),
    ("Hisobchi yetakchi mutaxasis", "Hisobchi yetakchi mutaxasis", ),
    ("Ekspert", "Ekspert", ),
)



class User(AbstractUser):
    uuid = models.CharField(max_length=1000, default=uuid4)
    pid = models.CharField(max_length=1000)
    username = models.CharField(max_length=1000, unique=True)
    full_name = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="images/users", null=True, blank=True)
    passport_number = models.CharField(max_length=1000)
    passport_pinfl = models.CharField(max_length=1000)
    branch = models.CharField(max_length=1000, choices=BRANCH)
    department = models.CharField(max_length=1000, choices=DEPARTMENT)
    position = models.CharField(max_length=1000, choices=POSITION)
    role = models.CharField(max_length=100, choices=ROLE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"
    objects = UserManager()

    def __str__(self):
        return self.username


class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    point = models.IntegerField(default=0)

    created = models.DateField()

    def __str__(self):
        return str(self.point)
    
    class Meta:
        unique_together = [["user", "created"]]


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_arrived = models.BooleanField(default=False)

    created = models.DateField()
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {'Kelgan' if self.is_arrived else 'Kelmagan'}"
    
    class Meta:
        unique_together = [["user", "created"]]


class Etiquette(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    point = models.CharField(max_length=10, default=3)

    created = models.DateField()
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.point)
    
    class Meta:
        unique_together = [["user", "created"]]


class Task(models.Model):
    uuid = models.CharField(max_length=100, default=uuid4, editable=False)
    name = models.CharField(max_length=2000)
    point = models.IntegerField(default=20)
    term = models.CharField(max_length=100, choices=TERM)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Submit(models.Model):
    uuid = models.CharField(max_length=100, default=uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    file = models.FileField(upload_to="files/tasks")
    status = models.CharField(max_length=100, choices=STATUS, default="in_process")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
class Application(models.Model):
    uuid = models.CharField(max_length=100, default=uuid4, editable=False)
    number = models.CharField(max_length=1000)
    file = models.FileField(upload_to="files/applications")
    status = models.CharField(max_length=100, choices=STATUS, default="created")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.number
