from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet, ModelForm

from .models import CourseProctoringService


class CheckBeforeDeleteFormset(BaseInlineFormSet):
    def clean(self):
        for form in self.forms:
            try:
                if getattr(form, "cleaned_data", {}).get('DELETE'):
                    form.validate_exam_content()

            except AttributeError:
                pass
        return super(CheckBeforeDeleteFormset, self).clean()


class CourseProctoringServiceForm(ModelForm):
    model = CourseProctoringService
    fields = '__all__'
    formset = CheckBeforeDeleteFormset

    def validate_exam_content(self):
        if self.instance.is_used_in_course():
            raise ValidationError(
                "%(service)s is used in %(course)s, change exams with service in course before deleting.",
                code="invalid",
                params={"service": str(self.instance.service), "course":str(self.instance.course)}
            )
