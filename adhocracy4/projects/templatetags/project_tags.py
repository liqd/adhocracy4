from django import template

register = template.Library()


@register.simple_tag
def project_tile_image(project):
    return project.tile_image or project.image or None


@register.simple_tag
def project_tile_image_copyright(project):
    if project.tile_image:
        return project.tile_image_copyright
    elif project.image:
        return project.image_copyright
    else:
        return None


@register.simple_tag
def project_tile_image_alt_text(project):
    if project.tile_image:
        return project.tile_image_alt_text
    elif project.image:
        return project.image_alt_text
    else:
        return None
