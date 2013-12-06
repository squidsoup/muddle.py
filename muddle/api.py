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
    """
    The main Muddle class

    Example Usage::

    >>> import muddle
    >>> course = muddle.course(int)
    <Response [200]>
    """

    def authenticate(self, api_key, api_url):
        Muddle.api_key = api_key
        Muddle.api_url = api_url + MOODLE_WS_ENDPOINT
        Muddle.request_params = {'wstoken': api_key,
                                 'moodlewsrestformat': 'json'}

    def course(self, *course_id):
        return Course(*course_id)

    def category(self, *category_id):
        return Category(*category_id)


class Course(Muddle):
    """ Represents API endpoints for a Moodle Course """

    def __init__(self, course_id=None):
        self.course_id = course_id

    def create(self, fullname, shortname, category_id, **kwargs):
        """
        Create a new course

        :param string fullname: The course's fullname
        :param string shortname: The course's shortname
        :param int category_id: The course's category

        :keyword string idnumber: (optional) Course ID number. \
            Yes, it's a string, blame Moodle.
        :keyword int summaryformat: (optional) Defaults to 1 (HTML). \
            Summary format options: (1 = HTML, 0 = Moodle, 2 = Plain, \
            or 4 = Markdown)
        :keyword string format: (optional) Defaults to "topics"
            Topic options: (weeks, topics, social, site)
        :keyword bool showgrades: (optional) Defaults to True. \
            Determines if grades are shown
        :keyword int newsitems: (optional) Defaults to 5. \
            Number of recent items appearing on the course page
        :keyword bool startdate: (optional) Timestamp when the course start
        :keyword int maxbytes: (optional) Defaults to 83886080. \
            Largest size of file that can be uploaded into the course
        :keyword bool showreports: Default to True. Are activity report shown?
        :keyword bool visible: (optional) Determines if course is \
            visible to students
        :keyword int groupmode: (optional) Defaults to 2.
            options: (0 = no group, 1 = separate, 2 = visible)
        :keyword bool groupmodeforce: (optional) Defaults to False. \
            Force group mode
        :keyword int defaultgroupingid: (optional) Defaults to 0. \
            Default grouping id
        :keyword bool enablecompletion: (optional) Enable control via \
            completion in activity settings.
        :keyword bool completionstartonenrol: (optional) \
            Begin tracking a student's progress in course completion after
        :keyword bool completionnotify: (optional) Default? Dunno. \
            Presumably notifies course completion
        :keyword string lang: (optional) Force course language.
        :keyword string forcetheme: (optional) Name of the force theme

        Example Usage::

        >>> import muddle
        >>> muddle.course().create('a new course', 'new-course', 20)
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
            option_params = {}
            for index, key in enumerate(kwargs):
                val = kwargs.get(key)

                if isinstance(val, bool):
                    val = int(val)

                option_params.update({'courses[0][' + key + ']': val})

            params = {'wsfunction': 'core_course_create_courses',
                      'courses[0][fullname]': fullname,
                      'courses[0][shortname]': shortname,
                      'courses[0][categoryid]': category_id}

            params.update(option_params)
            params.update(self.request_params)

            return requests.post(self.api_url, params=params, verify=False)

    def delete(self):
        """
        Deletes a specified courses

        Example Usage::

        >>> import muddle
        >>> muddle.course(10).delete()
        """

        params = {'wsfunction': 'core_course_delete_courses',
                  'courseids[0]': self.course_id}
        params.update(self.request_params)

        return requests.post(self.api_url, params=params, verify=False)

    def contents(self):
        """
        Returns entire contents of course page

        :returns: response object

        Example Usage::

        >>> import muddle
        >>> muddle.course(10).content()
        """

        params = self.request_params
        params.update({'wsfunction': 'core_course_get_contents',
                       'courseid': self.course_id})

        return requests.get(self.api_url, params=params, verify=False).json()

    def duplicate(self, fullname, shortname, categoryid,
                  visible=True, **kwargs):
        """
        Duplicates an existing course with options.
        Note: Can be very slow running.

        :param string fullname: The new course's full name
        :param string shortname: The new course's short name
        :param string categoryid: Category new course should be created under

        :keyword bool visible: Defaults to True. The new course's visiblity
        :keyword bool activities: (optional) Defaults to True. \
            Include course activites
        :keyword bool blocks: (optional) Defaults to True. \
            Include course blocks
        :keyword bool filters: (optional) Defaults to True. \
            Include course filters
        :keyword bool users: (optional) Defaults to False. Include users
        :keyword bool role_assignments: (optional) Defaults to False. \
            Include role assignments
        :keyword bool comments: (optional) Defaults to False. \
            Include user comments
        :keyword bool usercompletion: (optional) Defaults to False. \
            Include user course completion information
        :keyword bool logs: (optional) Defaults to False. Include course logs
        :keyword bool grade_histories: (optional) Defaults to False. \
            Include histories

        :returns: response object

        Example Usage::

        >>> import muddle
        >>> muddle.course(10).duplicate('new-fullname', 'new-shortname', 20)
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

    def export_data(self, export_to, delete_content=False):
        """
        Export course data to another course.
        Does not include any user data.

        :param bool delete_content: (optional) Delete content \
            from source course.

        Example Usage::

        >>> import muddle
        >>> muddle.course(10).export_data(12)
        """
        params = {'wsfunction': 'core_course_import_course',
                  'importfrom': self.course_id,
                  'importto': export_to,
                  'deletecontent': int(delete_content)}
        params.update(self.request_params)

        return requests.post(self.api_url, params=params, verify=False)


class Category(Muddle):
    """ Represents API endpoints for Moodle Courses Categories """

    def __init__(self, category_id=None):
        self.category_id = category_id

    def details(self):
        """
        Returns details for given category

        :returns: category response object

        Example Usage::

        >>> import muddle
        >>> muddle.category(10).details()
        """
        params = {'wsfunction': 'core_course_get_categories',
                  'criteria[0][key]': 'id',
                  'criteria[0][value]': self.category_id}

        params.update(self.request_params)

        return requests.post(self.api_url, params=params, verify=False)

    def create(self, category_name, **kwargs):
        """

        Create a new category

        :param string name: new category name
        :param int parent: (optional) Defaults to 0, root category. \
            The parent category id inside which the new \
            category will be created
        :param string description: (optional) The new category description
        :param int descriptionformat: (optional) Defaults to 1 \
            description format (1 = HTML,
                                0 = MOODLE,
                                2 = PLAIN,
                                4 = MARKDOWN)
        :param string theme: (optional) The new category theme

        Example Usage::

        >>> import muddle
        >>> muddle.category().create('category name')
        """
        allowed_options = ['parent',
                           'description',
                           'descriptionformat',
                           'theme']

        if valid_options(kwargs, allowed_options):
            option_params = {}
            for key in kwargs:
                option_params.update(
                    {'categories[0][' + key + ']': str(kwargs.get(key))})
            params = {'wsfunction': 'core_course_create_categories',
                      'categories[0][name]': category_name,
                      }
            params.update(option_params)
            params.update(self.request_params)

            return requests.post(self.api_url, params=params, verify=False)

    def delete(self, new_parent=None, recursive=False):
        """
        Deletes a category. Optionally moves content to new category.
        Note: If category is in root, new_parent must be specified.

        :param int new_parent: (optional) Category ID of new parent
        :param bool recursive: recursively delete contents inside this category

        Example Usage::

        >>> import muddle
        >>> muddle.category(10).delete()
        """

        params = {'wsfunction': 'core_course_delete_categories',
                  'categories[0][id]': self.category_id,
                  'categories[0][recursive]': int(recursive)}
        if new_parent:
            params.update({'categories[0][newparent]': new_parent})
        params.update(self.request_params)

        return requests.post(self.api_url, params=params, verify=False)

    def update_category(self):
        """
        core_course_update_categories
        Update categories
        """
        return NotImplemented
