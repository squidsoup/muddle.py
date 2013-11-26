import requests

MOODLE_WS_ENDPOINT = '/webservice/rest/server.php'


def valid_options(kwargs, allowed_options):
    """ Checks that kwargs are valid API options"""

    diff = set(kwargs) - set(allowed_options)
    if diff:
        print("Invalid option(s): ", ', '.join(diff))
        return False
    return True


class Muddle():
    """The main Muddle class"""

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

    def create(self, fullname, shortname, categoryid, **kwargs):
        """
        Create a new course

        :param string fullname: The course's fullname
        :param string shortname: The course's shortname
        :param int categoryid: The course's category

        :keyword string idnumber: Optional. Course ID number. \
            Yes, it's a string, blame Moodle.
        :keyword int summaryformat: Optional. Defaults to 1 (HTML). \
            Summary format options: (1 = HTML, 0 = Moodle, 2 = Plain, \
            or 4 = Markdown)
        :keyword string format: Optional. Defaults to "topics"
            Topic options: (weeks, topics, social, site)
        :keyword bool showgrades: Optional. Defaults to True. \
            Determines if grades are shown
        :keyword int newsitems: Optional. Defaults to 5. \
            Number of recent items appearing on the course page
        :keyword bool startdate: Optional. Timestamp when the course start
        :keyword int maxbytes: Optional. Defaults to 83886080. \
            Largest size of file that can be uploaded into the course
        :keyword bool showreports: Default to True. Are activity report shown?
        :keyword bool visible: Optional. Determines if course is \
            visible to students
        :keyword int groupmode: Optional. Defaults to 2.
            options: (0 = no group, 1 = separate, 2 = visible)
        :keyword bool groupmodeforce: Optional. Defaults to False. \
            Force group mode
        :keyword int defaultgroupingid: Optional. Defaults to 0. \
            Default grouping id
        :keyword bool enablecompletion: Optional. Enable control via \
            completion in activity settings.
        :keyword bool completionstartonenrol: Optional. \
            Begin tracking a student's progress in course completion after
        :keyword bool completionnotify: Optional. Default? Dunno. \
            Presumably notifies course completion
        :keyword string lang: Optional. Force course language.
        :keyword string forcetheme: Optional. Name of the force theme

        """

        allowed_options = ['idnumber', 'summaryformat',
                           'format', 'showgrades',
                           'newsitems', 'startdate',
                           'maxbytes', 'showreports',
                           'visible', 'groupmode',
                           'groupmodeforce', 'jdefaultgroupingid',
                           'enablecompletion', 'completionstartonenrol',
                           'completionnotify', 'lang',
                           'forcetheme']

        if valid_options(kwargs, allowed_options):
            params = {'wsfunction': 'core_course_create_courses',
                      'courseid': self.course_id}
            params.update(self.request_params)
        return NotImplemented

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

        :keyword bool visible: Defaults to True. The new course's visiblity
        :keyword bool activities: Optional. Defaults to True. \
            Include course activites
        :keyword bool blocks: Optional. Defaults to True. Include course blocks
        :keyword bool filters: Optional. Defaults to True. \
            Include course filters
        :keyword bool users: Optional. Defaults to False. Include users
        :keyword bool role_assignments: Optional. Defaults to False. \
            Include role assignments
        :keyword bool comments: Optional. Defaults to False. \
            Include user comments
        :keyword bool usercompletion: Optional. Defaults to False. \
            Include user course completion information
        :keyword bool logs: Optional. Defaults to False. Include course logs
        :keyword bool grade_histories: Optional. Defaults to False. \
            Include histories

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

        if valid_options(kwargs, allowed_options):
            option_params = {}
            for index, key in enumerate(kwargs):
                option_params.update(
                    {'options[' + str(index) + '][name]': key,
                     'options[' + str(index) + '][value]':
                        int(kwargs.get(key))})

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


class Category(Muddle):
    """ Represents API endpoints for Moodle Courses Categories """

    def __init__(self, course_ids):
        self.course_ids = course_ids

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
