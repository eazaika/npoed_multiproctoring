from django.db import models
from jsonfield.fields import JSONField
from openedx.core.djangoapps.xmodule_django.models import CourseKeyField


class ProctoringService(models.Model):
    class Meta:
        app_label = "npoed_multiproctoring"

    name = models.CharField(max_length=255)
    settings = JSONField(help_text="Settings for service")

    def __str__(self):
        return "<Service:{}>".format(self.name)


class CourseMultiproctoringState(models.Model):
    class Meta:
        app_label = "npoed_multiproctoring"
    course_id = CourseKeyField(max_length=255, db_index=True, unique=True, verbose_name='Course ID')

    def __str__(self):
        return "<Course: {}>".format(self.course_id)


class CourseProctoringService(models.Model):
    class Meta:
        app_label = "npoed_multiproctoring"
        unique_together = ("service", "course")
    service = models.ForeignKey(ProctoringService)
    course = models.ForeignKey(CourseMultiproctoringState)

    def __str__(self):
        return "<{}:{}>".format(self.course, self.service)

    def is_used_in_course(self):
        # TODO: make sane
        return self.service.name == 'dummy'

    def delete(self, using=None):
        return super(CourseProctoringService, self).delete(using)
