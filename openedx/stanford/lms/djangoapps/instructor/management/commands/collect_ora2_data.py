import csv
import optparse
import os
import tempfile

from django.core.management.base import BaseCommand, CommandError

from opaque_keys import InvalidKeyError
from opaque_keys.edx.locations import SlashSeparatedCourseKey

from openedx.stanford.lms.djangoapps.instructor_task.tasks_helper import collect_ora2_data


class Command(BaseCommand):
    """
    Query aggregated open assessment data, write to .csv
    """

    help = __doc__
    args = '<course_id>'
    option_list = BaseCommand.option_list + (
        optparse.make_option(
            '-o',
            '--output-dir',
            action='store',
            dest='output_dir',
            default=None,
            help='Write output to a directory rather than stdout',
        ),
    )

    def handle(self, *args, **options):
        if not args:
            raise CommandError("Course ID must be specified to fetch data")
        try:
            course_id = SlashSeparatedCourseKey.from_deprecated_string(args[0].decode('utf-8'))
        except InvalidKeyError:
            raise CommandError("The course ID given was invalid")
        file_name = "{course_id}-ora2.csv".format(
            course_id=course_id,
        )
        file_name = file_name.replace('/', '-')
        if options['output_dir']:
            csv_file = open(os.path.join(options['output_dir'], file_name), 'wb')
        else:
            csv_file = self.stdout
        writer = csv.writer(csv_file, dialect='excel', quotechar='"', quoting=csv.QUOTE_ALL)
        header, rows = collect_ora2_data(course_id)
        writer.writerow(header)
        for row in rows:
            writer.writerow(_preprocess(row))


def _preprocess(data_list):
    """
    Properly encode ora2 responses for transcription into a .csv
    """
    processed_data = []
    for item in data_list:
        new_item = unicode(item).encode('utf-8').encode('string_escape')
        new_item = new_item.replace("\"", "\\\"")
        processed_data.append(new_item)
    return processed_data
