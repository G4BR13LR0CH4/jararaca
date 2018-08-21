# Generated by Django 2.1 on 2018-08-21 17:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_auto_20180808_1829'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('uuid', models.UUIDField(default=uuid.UUID('73634e19-4f35-4909-a9be-c13d3a183a35'), editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500, verbose_name='name')),
                ('email', models.EmailField(max_length=50, verbose_name='email')),
                ('cpf', models.CharField(max_length=11, verbose_name='CPF')),
                ('share_data_with_partners', models.BooleanField(default=False, verbose_name='share data with partners')),
            ],
        ),
        migrations.CreateModel(
            name='EventDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='date')),
                ('start', models.TimeField(verbose_name='start time')),
                ('end', models.TimeField(verbose_name='end time')),
            ],
            options={
                'verbose_name': 'event day',
                'verbose_name_plural': 'event days',
            },
        ),
        migrations.CreateModel(
            name='EventDayCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entrance_date', models.DateTimeField(auto_now_add=True, verbose_name='entrance date/time')),
                ('exit_date', models.DateTimeField(null=True, verbose_name='exit date/time')),
                ('attendee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Attendee', verbose_name='attendee')),
                ('event_day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.EventDay', verbose_name='event day')),
            ],
            options={
                'verbose_name': 'event day check',
                'verbose_name_plural': 'event day checks',
            },
        ),
        migrations.CreateModel(
            name='EventSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.TimeField(verbose_name='start time')),
                ('end', models.TimeField(verbose_name='end time')),
                ('title', models.CharField(max_length=150, verbose_name='title')),
                ('place', models.CharField(blank=True, max_length=150, verbose_name='place')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('authors', models.CharField(blank=True, max_length=500, verbose_name='authors')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.EventDay', verbose_name='event day')),
            ],
            options={
                'verbose_name': 'event schedule',
                'verbose_name_plural': 'event schedules',
            },
        ),
        migrations.RemoveField(
            model_name='eventcheck',
            name='event',
        ),
        migrations.RemoveField(
            model_name='event',
            name='end',
        ),
        migrations.RemoveField(
            model_name='event',
            name='start',
        ),
        migrations.AddField(
            model_name='event',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete='created by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='latitude',
            field=models.FloatField(default=0, verbose_name='latitude'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='longitude',
            field=models.FloatField(default=0, verbose_name='longitude'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='organizers',
            field=models.CharField(default='', max_length=500, verbose_name='organizers'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='place',
            field=models.CharField(default='', max_length=500, verbose_name='place'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=500, verbose_name='name'),
        ),
        migrations.DeleteModel(
            name='EventCheck',
        ),
        migrations.AddField(
            model_name='eventday',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Event', verbose_name='event'),
        ),
        migrations.AddField(
            model_name='attendee',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Event', verbose_name='event'),
        ),
    ]