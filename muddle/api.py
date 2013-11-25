import requests
import sys

MOODLE_WS_ENDPOINT = "/webservice/rest/server.php"


class Muddle():
    """The main Muddle class."""

    def authenticate(self, api_key, api_url):
        Muddle.api_key = api_key
        Muddle.api_url = ''.join([api_url, MOODLE_WS_ENDPOINT])
        Muddle.request_params = {'wstoken': api_key,
                                 'moodlewsrestformat': 'json'}

    def course(self, course_id):
        return Course(course_id)

    def courses(self, course_ids=None):
        """ Returns list of all courses """

        #params = self.request_params
        #print(str(course_ids))
        #params.update({'wsfunction': 'core_course_get_courses',
        #               'options': str(course_ids)})
        #return requests.post(self.api_url, params=params, verify=False)
        return NotImplemented


class Course(Muddle):
    """ Represents API endpoints for Moodle Courses """

    def __init__(self, course_id):
        self.course_id = course_id

    @property
    def contents(self):
        """ Returns entire contents of course page """

        params = self.request_params
        params.update({'wsfunction': 'core_course_get_contents',
                       'courseid': self.course_id})
        return requests.get(self.api_url, params=params, verify=False).json()

    def duplicate(self, fullname, shortname, categoryid,
                  visible=True, **kwargs):
        ## Ideally categoryid should be optional here and
        ## should default to catid of course being duplicated.
        """
        Duplicate an existing course
        (creating a new one) without user data.

        REST (POST parameters)

        &options[1][key]=blocks&options[1][value]=1
        """
        allowed_options = ['activities', 'blocks',
                           'filters', 'users',
                           'role_assignments', 'comments',
                           'usercompletion', 'logs',
                           'grade_histories']

        diff = set(kwargs) - set(allowed_options)
        if diff:
            print("course.duplicate() - invalid option(s): ", ', '.join(diff))
            return

        option_params = {}
        for index, key in enumerate(kwargs):
            option_params.update(
                {'options[' + str(index) + '][name]': key,
                 'options[' + str(index) + '][value]': kwargs.get(key)})

        params = {'wsfunction': 'core_course_duplicate_course',
                  'courseid': self.course_id,
                  'fullname': fullname,
                  'shortname': shortname,
                  'categoryid': categoryid,
                  'visible': int(visible)}
        params.update(option_params)
        params.update(self.request_params)
        return requests.post(self.api_url, params=params, verify=False)

    def import_data(self):
        """
        core_course_import_course
        Import course data from a course into another course.
        Does not include any user data.
        """
        return NotImplemented

    def create(self):
        """
        Create new courses
        """
        params = self.request_params
        params.update({'wsfunction': 'core_course_create_courses',
                       'courseid': self.course_id})
        return NotImplemented

    def delete(self):
        """
        Deletes all specified courses
        core_course_delete_courses
        """
        return NotImplemented

    def categories(self):
        """
        core_course_get_categories
        Return category details
        """
        return NotImplemented

    def create_category(self):
        """
        core_course_create_categories
        Create course categories
        """
        return NotImplemented

    def update_category(self):
        """
        core_course_update_categories
        Update categories
        """

    def delete_category(self):
        """
        core_course_delete_categories
        Delete course categories
        """
        return NotImplemented
