"""
URL for enrollment API
"""
from django.conf.urls import patterns, url

from .views import UpdateEnrollmentView

urlpatterns = patterns(
    'enrollment.views',
    url(r'^update_status$', UpdateEnrollmentView.as_view(), name='updateenrollment'),
)
