# Generated by Django 4.0.5 on 2022-06-10 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0001_initial'),
        ('groups', '0001_initial'),
        ('workouts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workout',
            name='exercises',
        ),
        migrations.AddField(
            model_name='workout',
            name='exercises',
            field=models.ManyToManyField(related_name='workouts', to='exercises.exercise'),
        ),
        migrations.RemoveField(
            model_name='workout',
            name='groups',
        ),
        migrations.AddField(
            model_name='workout',
            name='groups',
            field=models.ManyToManyField(related_name='workouts', to='groups.group'),
        ),
    ]