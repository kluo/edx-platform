"""
API to update user enrollments
"""
from rest_framework.views import APIView
from rest_framework_oauth.authentication import OAuth2Authentication

from lms.djangoapps.instructor.enrollment import enroll_email
from openedx.core.lib.api.permissions import ApiKeyHeaderPermission
from openedx.core.djangoapps.cors_csrf.decorators import ensure_csrf_cookie_cross_domain


class UpdateEnrollmentView(APIView):
    """
    Update user enrollment for a particular course.
    """
    authentication_classes = OAuth2Authentication,
    permission_classes = (ApiKeyHeaderPermission,)

    @method_decorator(require_post_params(['email', 'course_id', 'action']))
    @method_decorator(ensure_csrf_cookie_cross_domain)
    def post(self, request):
        """
        Endpoint to update a user enrollment in a course.

        **Example Request**

            POST /api/enrollment/v1/update_status
            {
                'email': 'foo@bar.com',
                'course_id': 'course-v1:foo+bar+foobar',
                'action': 'enroll',
                'email_students': false,
                'auto_enroll': true
            }
        """
        email = request.data['email']
        course_id = request.data['course_id']
        action = request.data['action']
        email_students = request.data.get('email_students', False)
        auto_enroll = request.data.get('auto_enroll', False)

        enroll_email(
            course_id, email, auto_enroll, email_students, email_params, language=language
        )
