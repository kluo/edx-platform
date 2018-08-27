"""
URL for enrollment API
"""
from django.conf import settings
from django.conf.urls import patterns, url

from .views import EnrollmentStatusView

urlpatterns = patterns(
    'enrollment.views',
    url(
        r"^status/{course_key}/?$".format(
            course_key=settings.COURSE_ID_PATTERN,
        ),
        EnrollmentStatusView.as_view(),
        name='enrollment_status',
    ),
)
