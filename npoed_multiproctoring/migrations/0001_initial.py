# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import openedx.core.djangoapps.xmodule_django.models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourseMultiproctoringState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course_id', openedx.core.djangoapps.xmodule_django.models.CourseKeyField(unique=True, max_length=255, verbose_name=b'Course ID', db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseProctoringService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course', models.ForeignKey(to='npoed_multiproctoring.CourseMultiproctoringState')),
            ],
        ),
        migrations.CreateModel(
            name='ProctoringService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('settings', jsonfield.fields.JSONField(help_text=b'Settings for service')),
            ],
        ),
        migrations.AddField(
            model_name='courseproctoringservice',
            name='service',
            field=models.ForeignKey(to='npoed_multiproctoring.ProctoringService'),
        ),
    ]
