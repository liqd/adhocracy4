import re


class pytest_regex:
    """Assert that a given string meets some expectations."""

    def __init__(self, pattern, flags=0):
        self._regex = re.compile(pattern, flags)

    def __eq__(self, actual):
        return bool(self._regex.match(str(actual)))

    def __repr__(self):
        return self._regex.pattern


def setup_group_users(user_factory, group_factory, project):
    group1 = group_factory()
    group2 = group_factory()
    group3 = group_factory()
    group_member_in_orga = user_factory.create(groups=(group1, group2))
    group_member_out = user_factory.create(groups=(group2,))
    group_member_in_project = user_factory.create(groups=(group2, group3))

    project.organisation.groups.add(group1)
    project.group = group3
    project.save()

    return group_member_in_orga, group_member_out, group_member_in_project, \
        project
