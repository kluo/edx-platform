"""
Management command to dump CSV student responses for a course.
"""
import csv
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from opaque_keys import InvalidKeyError
from opaque_keys.edx.locations import SlashSeparatedCourseKey
from xmodule.modulestore.django import modulestore

from openedx.stanford.lms.djangoapps.instructor_task.tasks_helper import student_response_rows


class Command(BaseCommand):
    """
    Writes CSV student responses to all problems in specified course to
    specified file, or stdout by default.
    """
    args = '<course_id>'
    help = __doc__
    option_list = BaseCommand.option_list + (
        make_option(
            '-o',
            '--output-file',
            dest='filename',
            help='Write CSV to FILENAME, defaults to stdout',
        ),
    )

    def handle(self, *args, **options):
        def _utf8_encoded_rows(rows):
            for row in rows:
                yield [unicode(item).encode('utf-8') for item in row]

        if not args:
            raise CommandError("course_id not specified")
        store = modulestore()
        try:
            course_id = SlashSeparatedCourseKey.from_deprecated_string(args[0])
        except InvalidKeyError:
            raise CommandError("Invalid course_id")
        course = store.get_course(course_id)
        if course is None:
            raise CommandError("Invalid course_id")
        rows = student_response_rows(course)
        if not options['filename']:
            csvwriter = csv.writer(self.stdout, dialect='excel', quotechar='"', quoting=csv.QUOTE_ALL)
            csvwriter.writerows(_utf8_encoded_rows(rows))
        else:
            with open(options['filename'], 'wb') as csvfile:
                csvwriter = csv.writer(csvfile, dialect='excel', quotechar='"', quoting=csv.QUOTE_ALL)
                csvwriter.writerows(_utf8_encoded_rows(rows))
