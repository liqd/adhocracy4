from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from adhocracy4.models import base
from adhocracy4 import transforms as html_transforms
from adhocracy4.images import fields


class ProjectManager(models.Manager):

    def get_by_natural_key(self, name):
        return self.get(name=name)

    def featured(self):
        return self.filter(is_draft=False, is_archived=False)\
                   .order_by('-created')[:8]


class Project(base.TimeStampedModel):
    slug = AutoSlugField(populate_from='name', unique=True)
    name = models.CharField(
        max_length=120,
        verbose_name=_('Title of your project'),
        help_text=_('This title will appear on the '
                    'teaser card and on top of the project '
                    'detail page. It should be max. 120 characters long')
    )
    organisation = models.ForeignKey(
        settings.A4_ORGANISATIONS_MODEL,
        on_delete=models.CASCADE)
    description = models.CharField(
        max_length=250,
        verbose_name=_('Short description of your project'),
        help_text=_('This short description will appear on '
                    'the header of the project and in the teaser. '
                    'It should briefly state the goal of the project '
                    'in max. 250 chars.')
    )
    information = RichTextUploadingField(
        config_name='image-editor',
        verbose_name=_('Description of your project'),
        help_text=_('This description should tell participants '
                    'what the goal of the project is, how the project’s '
                    'participation will look like. It will be always visible '
                    'in the „Info“ tab on your project’s page.')
    )
    result = RichTextUploadingField(
        blank=True,
        config_name='image-editor',
        verbose_name=_('Results of your project'),
        help_text=_('Here you should explain what the expected outcome of the '
                    'project will be and how you are planning to use the '
                    'results. If the project is finished you should add a '
                    'summary of the results.')
    )
    is_public = models.BooleanField(
        default=True,
        verbose_name=_('Access to the project'),
        help_text=_('Please indicate who should be able to participate in '
                    'your project. Teasers for your project including title '
                    'and short description will always be visible to everyone')
    )
    is_draft = models.BooleanField(default=True)
    image = fields.ConfiguredImageField(
        'heroimage',
        verbose_name=_('Header image'),
        help_prefix=_(
            'The image will be shown as a decorative background image.'
        ),
        upload_to='projects/backgrounds',
        blank=True)
    tile_image = fields.ConfiguredImageField(
        'tileimage',
        verbose_name=_('Tile image'),
        help_prefix=_(
            'The image will be shown in the project tile.'
        ),
        upload_to='projects/tiles',
        blank=True)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='project_participant',
        blank=True,
    )
    moderators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='project_moderator',
        blank=True,
    )
    is_archived = models.BooleanField(
        default=False,
        verbose_name=_('Project is archived'),
        help_text=_('Set to archive the project'),
    )
    typ = models.CharField(
        max_length=120,
        verbose_name=_('Type of the project'),
        blank=True,
    )

    objects = ProjectManager()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.information = html_transforms.clean_html_field(
            self.information, 'image-editor')
        self.result = html_transforms.clean_html_field(
            self.result, 'image-editor')
        super(Project, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('project-detail', args=[str(self.slug)])

    def has_member(self, user):
        """
        Everybody is member of all public projects and private projects can
        be joined as moderator or participant.
        """
        return (
            (user.is_authenticated() and self.is_public)
            or (user in self.participants.all())
            or (user in self.moderators.all())
        )

    def has_moderator(self, user):
        return user in self.moderators.all()

    @property
    def other_projects(self):
        other_projects = self.organisation.project_set\
            .filter(is_draft=False, is_archived=False).exclude(slug=self.slug)
        return other_projects

    @property
    def is_private(self):
        return not self.is_public

    @property
    def modules(self):
        return self.module_set.all()

    @property
    def last_active_phase(self):
        """
        Return the last active phase.

        The last active phase is defined as the phase that out of all past
        and currently active phases ends last.
        """
        return self.phases\
            .past_and_active_phases()\
            .order_by('-end_date')\
            .first()

    @property
    def last_active_module(self):
        """Return the module of the last active phase."""
        last_active_phase = self.last_active_phase
        if last_active_phase:
            return last_active_phase.module
        return None

    @property
    def active_phase(self):
        """
        Return the currently active phase.

        The currently active phase is defined as the phase that out of all
        currently active phases ends last. This is analogous to the last
        active phase.

        Attention: This method is _deprecated_ as multiple phases may be
        active at the same time.
        """
        last_active_phase = self.last_active_phase
        if last_active_phase and not last_active_phase.is_over:
            return last_active_phase
        return None

    @property
    def days_left(self):
        """
        Return the number of days left in the currently active phase.

        Attention: This method is _deprecated_ as multiple phases may be
        active at the same time.
        """
        active_phase = self.active_phase
        if active_phase:
            today = timezone.now().replace(hour=0, minute=0, second=0)
            time_delta = active_phase.end_date - today
            return time_delta.days
        return None

    @property
    def phases(self):
        from adhocracy4.phases import models as phase_models
        return phase_models.Phase.objects.filter(module__project=self)

    @property
    def future_phases(self):
        return self.phases.future_phases()

    @property
    def past_phases(self):
        return self.phases.past_phases()

    @property
    def has_started(self):
        return self.phases.past_and_active_phases().exists()

    @property
    def has_finished(self):
        return not self.phases.active_phases().exists()\
               and not self.phases.future_phases().exists()

    @property
    def is_archivable(self):
        return not self.is_archived and self.has_finished
