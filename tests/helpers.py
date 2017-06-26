from django.contrib.auth.models import AnonymousUser


def setup_phase(phase_factory, item_factory, phase_content_class, **kwargs):
    phase_content = phase_content_class()
    phase = phase_factory(phase_content=phase_content, **kwargs)
    module = phase.module
    project = phase.module.project
    item = item_factory(module=module) if item_factory else None
    return phase, module, project, item


def setup_users(project):
    anonymous = AnonymousUser()
    moderator = project.moderators.first()
    initiator = project.organisation.initiators.first()
    return anonymous, moderator, initiator
