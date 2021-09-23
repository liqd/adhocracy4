from adhocracy4.polls import exports as a4_poll_exports


class PollCommentExportView(a4_poll_exports.PollCommentExportView):

    permission_required = 'a4projects.change_project'

    def get_permission_object(self):
        return self.module.project


class PollExportView(a4_poll_exports.PollExportView):

    permission_required = 'a4projects.change_project'

    def get_permission_object(self):
        return self.module.project
