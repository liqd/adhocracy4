import pytest
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponse

from adhocracy4.projects import views
from adhocracy4.test.helpers import redirect_target

from unittest import mock


@pytest.mark.django_db
def test_detail_view(client, project):
    project_url = reverse('project-detail', args=[project.slug])
    response = client.get(project_url)
    assert response.status_code == 200
    assert response.context_data['view'].project == project


@pytest.mark.django_db
@pytest.mark.parametrize('project__is_public', [False])
def test_detail_private_project(client, project, user):
    project_url = reverse('project-detail', args=[project.slug])
    response = client.get(project_url)
    assert response.status_code == 302
    assert redirect_target(response) == 'account_login'

    client.login(username=user, password='password')
    response = client.get(project_url)
    assert response.status_code == 403

    project.participants.add(user)
    response = client.get(project_url)
    assert response.status_code == 200
    assert response.context_data['view'].project == project


@pytest.mark.django_db
@pytest.mark.parametrize('project__is_draft', [True])
def test_detail_draft_project(client, project, user, staff_user):
    project_url = reverse('project-detail', args=[project.slug])
    response = client.get(project_url)
    assert response.status_code == 302
    assert redirect_target(response) == 'account_login'

    client.login(username=user, password='password')
    response = client.get(project_url)
    assert response.status_code == 403

    client.login(username=staff_user, password='password')
    response = client.get(project_url)
    assert response.status_code == 200
    assert response.context_data['view'].project == project


def dispatch_view(view_class, request, *args, **kwargs):
    """Mimic as_view() and dispatch() but returns view instance in addition."""
    view = view_class()
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view.dispatch(request, *args, **kwargs), view


class FakeProjectContextView(views.ProjectContextDispatcher):
    def get(self, request, *args, **kwargs):
        return HttpResponse('project_context')


@pytest.mark.django_db
def test_project_context_kwargs(rf, project):
    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextView, request,
                                   project=project)

    assert response.content == b'project_context'
    assert view.project == project


@pytest.mark.django_db
def test_project_context_url(rf, project):
    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextView, request,
                                   project_slug=project.slug)

    assert response.content == b'project_context'
    assert view.project == project


@pytest.mark.django_db
def test_project_context_url_overwrite(rf, project):
    class FakeProjectContextViewUrlOverwrite(FakeProjectContextView):
        project_lookup_field = 'id'
        project_url_kwarg = 'project_id'

    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextViewUrlOverwrite, request,
                                   project_id=project.id)

    assert response.content == b'project_context'
    assert view.project == project


@pytest.mark.django_db
def test_project_context_object(rf, project):
    class FakeProjectContextGetObjectView(FakeProjectContextView):
        def get_object(self):
            return mock.Mock(project=project, module=None)

    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextGetObjectView, request)

    assert response.content == b'project_context'
    assert view.project == project


@pytest.mark.django_db
def test_project_context_project_object(rf, project):
    class FakeProjectContextGetObjectView(FakeProjectContextView):
        def get_object(self):
            return project

    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextGetObjectView, request)

    assert response.content == b'project_context'
    assert view.project == project


@pytest.mark.django_db
def test_project_context_overwrite(rf, project):
    class FakeProjectContextGetProjectView(FakeProjectContextView):
        def get_project(self, *args, **kwargs):
            return project

    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextGetProjectView,
                                   request)

    assert response.content == b'project_context'
    assert view.project == project


@pytest.mark.django_db
def test_project_context_missing(rf):
    request = rf.get('/url')
    with pytest.raises(Http404):
        dispatch_view(FakeProjectContextView, request)


@pytest.mark.django_db
def test_project_context_invalid(rf, project_factory):
    class FakeProjectContextViewInvalid(FakeProjectContextView):
        def get_project(self, *args, **kwargs):
            return project_factory()

        def get_object(self):
            return mock.Mock(project=project_factory())

    request = rf.get('/url')
    with pytest.raises(PermissionDenied):
        dispatch_view(FakeProjectContextViewInvalid, request)


@pytest.mark.django_db
def test_project_template_context(rf, project):
    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextView,
                                   request, project=project)

    context = view.get_context_data()
    assert context['project'] == project


@pytest.mark.django_db
def test_module_context_kwargs(rf, module):
    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextView,
                                   request, module=module)

    assert response.content == b'project_context'
    assert view.module == module
    assert view.project == module.project


@pytest.mark.django_db
def test_module_context_url(rf, module):
    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextView,
                                   request,
                                   module_slug=module.slug)

    assert response.content == b'project_context'
    assert view.module == module


@pytest.mark.django_db
def test_module_context_url_overwrite(rf, module):
    class FakeProjectContextViewUrlOverwrite(FakeProjectContextView):
        module_lookup_field = 'id'
        module_url_kwarg = 'module_id'

    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextViewUrlOverwrite, request,
                                   module_id=module.id)

    assert response.content == b'project_context'
    assert view.module == module


@pytest.mark.django_db
def test_module_context_object(rf, module):
    class FakeProjectContextGetObjectView(FakeProjectContextView):
        def get_object(self):
            return mock.Mock(module=module, project=None)

    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextGetObjectView, request)

    assert response.content == b'project_context'
    assert view.module == module


@pytest.mark.django_db
def test_module_context_module_object(rf, module):
    class FakeProjectContextGetObjectView(FakeProjectContextView):
        def get_object(self):
            return module

    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextGetObjectView, request)

    assert response.content == b'project_context'
    assert view.module == module


@pytest.mark.django_db
def test_module_context_overwrite(rf, module):
    class FakeProjectContextGetProjectView(FakeProjectContextView):
        def get_module(self, *args, **kwargs):
            return module

    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextGetProjectView, request)

    assert response.content == b'project_context'
    assert view.module == module


@pytest.mark.django_db
def test_module_context_invalid(rf, module_factory):
    class FakeProjectContextViewInvalid(FakeProjectContextView):
        def get_project(self, *args, **kwargs):
            return module_factory()

        def get_object(self):
            return mock.Mock(module=module_factory())

    request = rf.get('/url')
    with pytest.raises(PermissionDenied):
        dispatch_view(FakeProjectContextViewInvalid, request)


@pytest.mark.django_db
def test_module_template_context(rf, module):
    request = rf.get('/url')
    response, view = dispatch_view(FakeProjectContextView,
                                   request, module=module)

    context = view.get_context_data()
    assert context['module'] == module
