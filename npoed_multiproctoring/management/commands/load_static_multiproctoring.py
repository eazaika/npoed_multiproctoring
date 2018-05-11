import pkgutil
import shutil
from io import StringIO
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


def get_package_file_stream(x):
    name = 'static/' + x
    return StringIO(unicode(pkgutil.get_data("npoed_multiproctoring", name)))


def get_edx_file_stream(x):
    names = x.split(".")
    filename = ".".join(names[-2:])
    addr = _EDX_PLATFORM + "/".join(names[:-2]) + "/"+  filename
    return open(addr, 'w')


_EDX_PLATFORM = "/edx/app/edxapp/edx-platform/"
_STATIC = [
    "cms.static.js.views.modals.course_outline_modals.js",
    "cms.templates.js.timed-examination-preference-editor.underscore"
]


class Command(BaseCommand):
    """
    This command loads static files from package to edx. It's supposed
    that there is no difference in them since ginkgo release.
    """
    KEY = "ENABLE_MULTIPROCTORING"
    help = "Loads static for multiproctoring feature. Edx default static is replaced!"\
           "Example:" \
           "'./manage.py lms load_static_multiproctoring --settings=SETTINGS'"

    def handle(self, *args, **kwargs):  # pylint: disable=unused-argument
        self.load_static()

    def load_static(self):
        if not settings.FEATURES.get(self.KEY):
            message = "Feature '{}' is not enabled in django settings."" \
            ""Add key '{}' with value True, then run command again".format(self.KEY, self.KEY)
            raise CommandError(message)

        for name in _STATIC:
            f = get_package_file_stream(name)
            g = get_edx_file_stream(name)
            shutil.copyfileobj(f, g)
        message = "Static were loaded successfully"
        self.stdout.write(
            message
        )