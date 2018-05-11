Description
-----------

It was tested on `Ginkgo release
<https://github.com/edx/edx-platform/tree/open-release/ginkgo.master>`_

Installation
------------

1. Install this package, add it into the INSTALLED_APPS and run migrations if it is not done yet.

   ::

     python -m pip install -e git+https://github.com/miptliot/npoed_multiproctoring.git#egg=npoed-multiproctoring
     python manage.py lms migrate npoed_multiproctoring --settings=YOUR_SETTINGS

2. Apply decorator 'enable_npoed_multiproctoring' to the next classes/functions

    * common.lib.xmodule.xmodule.seq.py: ProctoringFields
    * cms.djangoapps.contentstore.views.item.py: create_xblock_info
    * cms.djangoapps.models.settings.py: CourseMetadata

  Example:
  ::

     ...
     from npoed_multiproctoring import enable_npoed_multiproctoring

     @enable_npoed_multiproctoring
     class CourseMetadata(object):
     ...

3. Enable feature in lms and cms settings

  ::

    FEATURES["ENABLE_MULTIPROCTORING"] = True


4. Run django command

  ::

    python manage.py lms load_static_multiproctoring --settings=SETTINGS


  Or copy static files manually from static/


6. At the admin dashboard find npoed_multiproctoring, add Proctoring Services and connect them with course in 'Course multiproctoring states'.


7. (Optional) Update staticfiles
