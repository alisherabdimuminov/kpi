# Generated by Django 5.1.4 on 2024-12-15 07:52

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('approved', 'Tasdiqlangan'), ('rejected', 'Rad etilgan'), ('in_process', 'Jarayonda'), ('created', 'Yaratilgan')], default='created', max_length=100),
        ),
        migrations.AlterField(
            model_name='application',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='submit',
            name='status',
            field=models.CharField(choices=[('approved', 'Tasdiqlangan'), ('rejected', 'Rad etilgan'), ('in_process', 'Jarayonda'), ('created', 'Yaratilgan')], default='in_process', max_length=100),
        ),
        migrations.AlterField(
            model_name='task',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=100),
        ),
    ]