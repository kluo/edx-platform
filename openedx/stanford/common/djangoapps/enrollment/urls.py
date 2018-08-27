"""
URL for enrollment API
"""
from django.conf.urls import patterns, url

from .views import EnrollmentStatusView

urlpatterns = patterns(
    'enrollment.views',
    url(
        r'^enrollment/status/{course_key}/?$',
        EnrollmentStatusView.as_view(),
        name='updateenrollment',
    ),
)
