from functools import wraps
from xblock.fields import Scope, String, Dict
from django.conf import settings
from .models import CourseMultiproctoringState
_ = lambda text: text


def build_create_xblock_info(func):
    @wraps(func)
    def wrap(xblock, *args, **kwargs):
        info = func(xblock, *args, **kwargs)
        if xblock.category == 'sequential':
            course_id = xblock.location.course_key
            info.update({
                'exam_review_checkbox': xblock.exam_review_checkbox,
                'proctoring_services': CourseMultiproctoringState.get_service_names(course_id),
                'exam_proctoring_system': xblock.exam_proctoring_system,
            })
        return info
    return wrap


def build_CourseMetadata(cls):
    cls.FILTERED_LIST.extend(['exam_review_checkbox', 'exam_proctoring_system'])
    return cls


def build_ProctoringFields(cls):
    class MultiProctoringFields(cls):
        exam_review_checkbox = Dict(
            display_name=_("exam_review_checkbox"),
            help=_(
                "exam_review_checkbox"
            ),
            default={
                 "calculator": True,
                 "excel": False,
                 "messengers": False,
                 "absence": False,
                 "books": False,
                 "papersheet": True,
                 "aid": False,
                 "web_sites": False,
                 "voice": False,
                 "gaze_averted": True
            },
            scope=Scope.settings,
        )

        exam_proctoring_system = String(
            display_name=_("Proctoring system"),
            help=_(""),
            default='',
            scope=Scope.settings,
        )

        @property
        def available_proctoring_services(self):
            """
            Returns the list of proctoring services for the course if available, else None
            """
            # TODO: find all places where this called and refactor them
            string = ",".join(CourseMultiproctoringState.get_service_names(self.location.course_key))
            return string
    return MultiProctoringFields


replaced = {
    "create_xblock_info": build_create_xblock_info,
    "CourseMetadata": build_CourseMetadata,
    "ProctoringFields": build_ProctoringFields
}


def enable_npoed_multiproctoring(obj):
    if not settings.FEATURES.get("ENABLE_MULTIPROCTORING", False):
        return obj
    name = obj.__name__
    if name in replaced:
        constructor = replaced.get(name)
        return constructor(obj)
    return obj