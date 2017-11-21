from meinberlin.apps.dashboard2 import views as a4dashboard_views


class DashboardProjectListView(a4dashboard_views.ProjectListView):
    def get_queryset(self):
        return super().get_queryset().filter(projectcontainer=None)
