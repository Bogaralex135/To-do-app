# Generated by Django 4.1.7 on 2023-03-13 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskList', '0003_rename_date_task_reminder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='reminder',
        ),
    ]
