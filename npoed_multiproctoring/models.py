import logging
from django.db import models
from jsonfield.fields import JSONField
from openedx.core.djangoapps.xmodule_django.models import CourseKeyField
from xmodule.modulestore.django import modulestore


log = logging.getLogger(__name__)

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

    @classmethod
    def get_service_names(cls, course_id):
        query = cls.objects.filter(course_id=course_id)
        if not len(query):
            return []
        instance = query.first()
        return [x.name for x in instance.services.all()]


class CourseProctoringService(models.Model):
    class Meta:
        app_label = "npoed_multiproctoring"
        unique_together = ("service", "course")
    service = models.ForeignKey(ProctoringService)
    course = models.ForeignKey(CourseMultiproctoringState, related_name='services')

    def __str__(self):
        return "<{}:{}>".format(self.course, self.service)

    def is_used_in_course(self):
        course_key = self.course.course_id
        proctoring_name = self.service.name
        store = modulestore()
        if not store.has_course(course_key):
            log.error("Multiproctoring is setup for non-existent course")
            return False
        sequentials = modulestore().get_items(
            course_key,
            qualifiers={'category': 'sequential'}
        )
        for x in sequentials:
            if x.is_proctored_exam and getattr(x, 'exam_proctoring_system', None) == proctoring_name:
                return True
        return False

    @property
    def name(self):
        return self.service.name
