import requests

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

    def courses(self, course_ids):
        return Courses(course_ids)


class Courses(Muddle):
    """ Represents API endpoints for Moodle Courses """

    def __init__(self, course_ids):
        self.course_ids = course_ids

    def delete(self):
        """
        Deletes all specified courses
        """

        option_params = {}
        for index, id in enumerate(self.course_ids):
            option_params.update(
                {'courseids[' + str(index) + ']': id})

        params = {'wsfunction': 'core_course_delete_courses'}
        params.update(option_params)
        params.update(self.request_params)

        return requests.post(self.api_url, params=params, verify=False)


class Course(Muddle):
    """ Represents API endpoints for a Moodle Course """

    def __init__(self, course_id):
        self.course_id = course_id

    @property
    def contents(self):
        """
        Returns entire contents of course page

        :returns: response object
        """

        params = self.request_params
        params.update({'wsfunction': 'core_course_get_contents',
                       'courseid': self.course_id})
        return requests.get(self.api_url, params=params, verify=False).json()

    def duplicate(self, fullname, shortname, categoryid,
                  visible=True, **kwargs):
        """
        Duplicates an existing course with options.

        :param string fullname: The new course's full name
        :param string shortname: The new course's short name
        :param string categoryid: Category new course should be created under

        :keyword bool visible: The new course's visiblity
        :keyword bool activities: Include course activites
        :keyword bool blocks: Include course blocks
        :keyword bool filters: Include course filters
        :keyword bool users: Include users
        :keyword bool role_assignments: Include role assignments
        :keyword bool comments: Include user comments
        :keyword bool usercompletion: Inclue user course completion information
        :keyword bool logs: Include course logs
        :keyword bool grade_histories: Include histories

        :returns: response object
        """

        # TODO
        # Ideally categoryid should be optional here and
        # should default to catid of course being duplicated.

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
                 'options[' + str(index) + '][value]': int(kwargs.get(key))})

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
