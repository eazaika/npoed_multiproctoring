from django.contrib import admin

from .forms import CheckBeforeDeleteFormset, CourseProctoringServiceForm
from .models import ProctoringService, CourseProctoringService, CourseMultiproctoringState


@admin.register(ProctoringService)
class ProctoringServiceAdmin(admin.ModelAdmin):
    pass


class CourseProctoringServiceInlineAdmin(admin.StackedInline):
    model = CourseProctoringService
    form = CourseProctoringServiceForm
    formset = CheckBeforeDeleteFormset


@admin.register(CourseMultiproctoringState)
class CourseProctoringServiceStateAdmin(admin.ModelAdmin):
    inlines = [CourseProctoringServiceInlineAdmin]
