import warnings

from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django_enumfield.enum import EnumField

from adhocracy4 import transforms as html_transforms
from adhocracy4.administrative_districts.models import AdministrativeDistrict
from adhocracy4.ckeditor.fields import RichTextCollapsibleUploadingField
from adhocracy4.images import fields
from adhocracy4.maps.fields import PointField
from adhocracy4.models import base

from .enums import Access
from .fields import TopicField
from .utils import get_module_clusters
from .utils import get_module_clusters_dict


class ProjectManager(models.Manager):

    def get_by_natural_key(self, name):
        return self.get(name=name)

    def featured(self):
        return self.filter(is_draft=False, is_archived=False)\
                   .order_by('-created')[:8]


class ProjectContactDetailMixin(models.Model):
    class Meta:
        abstract = True

    phone_regex = RegexValidator(
        regex=r'^[\d\+\(\)\- ]{8,20}$',
        message=_("Phone numbers can only contain digits, spaces and "
                  "the following characters: -, +, (, ). "
                  "It has to be between 8 and 20 characters long."))

    contact_address_text = models.TextField(
        blank=True,
        verbose_name=_('Postal address')
    )

    contact_email = models.EmailField(
        blank=True)

    contact_name = models.CharField(
        max_length=120,
        blank=True,
        verbose_name=_('Contact person')
    )

    contact_phone = models.CharField(
        validators=[phone_regex],
        max_length=20,
        blank=True
    )

    contact_url = models.URLField(
        blank=True)


class ProjectLocationMixin(models.Model):
    class Meta:
        abstract = True

    point = PointField(
        null=True,
        blank=True,
        verbose_name=_('Can your project be located on the map?'),
        help_text=_('Locate your project. '
                    'Click inside the marked area '
                    'or type in an address to set the marker. A set '
                    'marker can be dragged when pressed.')
    )

    administrative_district = models.ForeignKey(
        AdministrativeDistrict,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_('Administrative district')
    )


class ModuleClusterPropertiesMixin:

    @cached_property
    def module_clusters(self):
        modules = self.module_set.filter(is_draft=False)
        return get_module_clusters(modules)

    @cached_property
    def module_cluster_dict(self):
        return get_module_clusters_dict(self.module_clusters)

    @cached_property
    def running_modules(self):
        return self.modules.running_modules()


class TimelinePropertiesMixin:

    def get_events_list(self):
        if self.events:
            return self.events.values('date', 'name',
                                      'event_type',
                                      'slug', 'description')
        return []

    @cached_property
    def participation_dates(self):
        module_clusters = self.module_cluster_dict
        event_list = self.get_events_list()
        full_list = module_clusters + list(event_list)
        return sorted(full_list, key=lambda k: k['date'])

    @cached_property
    def display_timeline(self):
        return len(self.participation_dates) > 1

    def get_current_participation_date(self):
        now = timezone.now()
        for idx, val in enumerate(self.participation_dates):
            if 'type' in val and val['type'] == 'module':
                start_date = val['date']
                end_date = val['end_date']
                if start_date and end_date:
                    if now >= start_date and now <= end_date:
                        return idx
        for idx, val in enumerate(self.participation_dates):
            date = val['date']
            if date:
                if now <= date:
                    return idx

    def get_current_event(self, idx):
        pd = self.participation_dates
        try:
            current_dict = pd[idx]
            if 'type' not in current_dict:
                return current_dict
        except (IndexError, KeyError):
            return []
        return []

    def get_current_modules(self, idx):
        pd = self.participation_dates
        try:
            current_dict = pd[idx]
            if current_dict['type'] == 'module':
                return current_dict['modules']
        except (IndexError, KeyError):
            return []
        return []


class Project(ProjectContactDetailMixin,
              ProjectLocationMixin,
              base.TimeStampedModel,
              ModuleClusterPropertiesMixin,
              TimelinePropertiesMixin):
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

    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True)

    description = models.CharField(
        max_length=250,
        verbose_name=_('Short description of your project'),
        help_text=_('This short description will appear on '
                    'the header of the project and in the teaser. '
                    'It should briefly state the goal of the project '
                    'in max. 250 chars.')
    )
    information = RichTextCollapsibleUploadingField(
        blank=True,
        config_name='collapsible-image-editor',
        verbose_name=_('Description of your project'),
        help_text=_('This description should tell participants '
                    'what the goal of the project is, how the project’s '
                    'participation will look like. It will be always visible '
                    'in the „Info“ tab on your project’s page.')
    )
    result = RichTextCollapsibleUploadingField(
        blank=True,
        config_name='collapsible-image-editor',
        verbose_name=_('Results of your project'),
        help_text=_('Here you should explain what the expected outcome of the '
                    'project will be and how you are planning to use the '
                    'results. If the project is finished you should add a '
                    'summary of the results.')
    )
    access = EnumField(
        Access,
        default=Access.PUBLIC,
        verbose_name=_('Access to the project')
    )
    is_draft = models.BooleanField(default=True)
    image = fields.ConfiguredImageField(
        'heroimage',
        verbose_name=_('Header image'),
        help_prefix=_(
            'The image will be shown as a decorative background image.'
        ),
        upload_to='projects/backgrounds',
        blank=True,
        max_length=300)
    image_copyright = fields.ImageCopyrightField(image_name=_('Header image'))
    tile_image = fields.ConfiguredImageField(
        'tileimage',
        verbose_name=_('Tile image'),
        help_prefix=_(
            'The image will be shown in the project tile.'
        ),
        upload_to='projects/tiles',
        blank=True,
        max_length=300)
    tile_image_copyright = fields.ImageCopyrightField(
        image_name=_('Tile image'))
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
        help_text=_('Archived projects are not shown in the project overview. '
                    'For project initiators they are still visible in the '
                    'dashboard.'),
    )
    topics = TopicField(
        verbose_name=_('Project topics'),
        help_text=_('Add topics to your project.')
    )
    project_type = models.CharField(
        blank=True,
        max_length=256,
        default='a4projects.Project'
    )

    is_app_accessible = models.BooleanField(default=False)

    objects = ProjectManager()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.information = html_transforms.clean_html_field(
            self.information, 'collapsible-image-editor')
        self.result = html_transforms.clean_html_field(
            self.result, 'collapsible-image-editor')
        if self.pk is None:
            project_type = '{}.{}'.format(
                self._meta.app_label,
                self.__class__.__name__
            )
            self.project_type = project_type
        super(Project, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('project-detail', kwargs=dict(slug=self.slug))

    # functions needed to determine permissions
    def has_member(self, user):
        """
        Everybody is member of all public projects and private projects can
        be joined as moderator or participant.
        """
        return (
            (user.is_authenticated and self.is_public)
            or (user in self.participants.all())
            or (user in self.moderators.all())
        )

    def is_group_member(self, user):
        if self.group:
            return user.groups.filter(id=self.group.id).exists()
        return False

    def has_moderator(self, user):
        return user in self.moderators.all()

    # properties
    @cached_property
    def topic_names(self):
        if hasattr(settings, 'A4_PROJECT_TOPICS'):
            choices = dict(settings.A4_PROJECT_TOPICS)
            return [choices[topic] for topic in self.topics]
        return []

    @cached_property
    def other_projects(self):
        other_projects = self.organisation.project_set\
            .filter(is_draft=False, is_archived=False).exclude(slug=self.slug)
        return other_projects

    @cached_property
    def is_private(self):
        return self.access == Access.PRIVATE

    @cached_property
    def is_public(self):
        return self.access == Access.PUBLIC

    @cached_property
    def is_semipublic(self):
        return self.access == Access.SEMIPUBLIC

    @cached_property
    def is_archivable(self):
        return not self.is_archived and self.has_finished

    # module properties
    @cached_property
    def modules(self):
        return self.module_set.all()

    @cached_property
    def published_modules(self):
        return self.module_set.filter(is_draft=False)

    @cached_property
    def unpublished_modules(self):
        return self.module_set.filter(is_draft=True)

    @cached_property
    def running_module_ends_next(self):
        """
        Return the currently active module that ends next.
        """
        return self.running_modules.order_by('module_end').first()

    @cached_property
    def past_modules(self):
        """Return past modules ordered by start."""
        return self.published_modules.past_modules()

    @cached_property
    def future_modules(self):
        """
        Return future modules ordered by start date.

        Note: Modules without a start date are assumed to start in the future.
        """
        return self.published_modules.future_modules()

    @cached_property
    def module_running_days_left(self):
        """
        Return the number of days left in the currently running module that
        ends next.

        Attention: It's a bit coarse and should only be used for estimations
        like 'ending soon', but NOT to display the number of days a project
        is still running. For that use module_running_time_left.
        """
        running_module = self.running_module_ends_next
        if running_module:
            today = timezone.now().replace(hour=0, minute=0, second=0)
            time_delta = running_module.module_end - today
            return time_delta.days
        return None

    @cached_property
    def module_running_time_left(self):
        """
        Return the time left in the currently running module that ends next.
        """

        running_module = self.running_module_ends_next
        if running_module:
            return running_module.module_running_time_left
        return None

    @cached_property
    def module_running_progress(self):
        """
        Return the progress of the currently running module that ends next
        in percent.
        """
        running_module = self.running_module_ends_next
        if running_module:
            return running_module.module_running_progress
        return None

    # properties used in timeline/module cluster logic
    @cached_property
    def end_date(self):
        # FIXME: project properties should rely on modules, not phases.
        end_date = None
        last_phase = self.published_phases.exclude(end_date=None)\
            .order_by('end_date').last()
        if last_phase and last_phase.end_date:
            end_date = last_phase.end_date
        if self.events:
            last_event = self.events.order_by('date').last()
            if end_date:
                if last_event.date > end_date:
                    end_date = last_event.date
            else:
                end_date = last_event.date
        return end_date

    @cached_property
    def events(self):
        if hasattr(self, 'offlineevent_set'):
            return self.offlineevent_set.all()

    @cached_property
    def has_future_events(self):
        if self.events:
            now = timezone.now()
            return self.events.filter(date__gt=now).exists()
        return False

    # properties relying on phases
    @cached_property
    def last_active_phase(self):
        """
        Return the last active phase.

        The last active phase is defined as the phase that out of all past
        and currently active phases started last.
        This property is used to determine which phase view is shown.
        """
        # FIXME: project properties should rely on modules, not phases.
        return self.phases\
            .filter(module__is_draft=False)\
            .past_and_active_phases()\
            .last()

    @cached_property
    def last_active_module(self):
        """
        Return the module of the last active phase.

        Attention: Might be _deprecated_ and replaced by logic coming from
        the modules.
        """
        # FIXME: project properties should rely on modules, not phases.
        last_active_phase = self.last_active_phase
        if last_active_phase:
            return last_active_phase.module
        return None

    @cached_property
    def active_phase_ends_next(self):
        """
        Return the currently active phase that ends next.
        """
        # FIXME: project properties should rely on modules, not phases.
        return self.phases.active_phases()\
            .filter(module__is_draft=False)\
            .order_by('end_date').first()

    @cached_property
    def phases(self):
        # FIXME: project properties should rely on modules, not phases.
        from adhocracy4.phases import models as phase_models
        return phase_models.Phase.objects\
            .filter(module__project=self)

    @cached_property
    def published_phases(self):
        # FIXME: project properties should rely on modules, not phases.
        from adhocracy4.phases import models as phase_models
        return phase_models.Phase.objects\
            .filter(module__project=self, module__is_draft=False)

    @cached_property
    def future_phases(self):
        # FIXME: project properties should rely on modules, not phases.
        return self.published_phases.future_phases()

    @cached_property
    def past_phases(self):
        # FIXME: project properties should rely on modules, not phases.
        return self.published_phases.past_phases()

    @cached_property
    def has_started(self):
        # FIXME: project properties should rely on modules, not phases.
        return self.published_phases.past_and_active_phases().exists()

    @cached_property
    def has_finished(self):
        # FIXME: project properties should rely on modules, not phases.
        return self.modules.exists()\
            and self.published_modules.exists()\
            and not self.published_phases.active_phases().exists()\
            and not self.published_phases.future_phases().exists()\
            and not self.has_future_events

    # deprecated properties
    @cached_property
    def active_phase(self):
        """
        Return the currently active phase.

        The currently active phase is defined as the phase that out of all
        currently active phases started last. This is analogous to the last
        active phase.

        Attention: This method is _deprecated_ as multiple phases (in
        different modules) may be active at the same time.
        """
        warnings.warn(
            "active_phase is deprecated; "
            "use active_phase_ends_next or active_module_ends_next",
            DeprecationWarning
        )
        last_active_phase = self.last_active_phase
        if last_active_phase and not last_active_phase.is_over:
            return last_active_phase
        return None

    @cached_property
    def days_left(self):
        """
        Return the number of days left in the currently active phase.

        Attention: This method is _deprecated_ as multiple phases may be
        active at the same time.
        """
        warnings.warn(
            "days_left is deprecated as it relies on active_phase; "
            "use module_running_days_left",
            DeprecationWarning
        )
        active_phase = self.active_phase
        if active_phase:
            today = timezone.now().replace(hour=0, minute=0, second=0)
            time_delta = active_phase.end_date - today
            return time_delta.days
        return None

    @cached_property
    def time_left(self):
        """
        Return the time left in the currently active phase that ends next.

        Attention: _deprecated_ as in the projects logic from the modules
        should be used.
        """
        warnings.warn(
            "time_left is deprecated as in the projects "
            "logic from the modules should be used; "
            "use module_running_time_left",
            DeprecationWarning
        )

        def seconds_in_units(seconds):
            unit_totals = []

            unit_limits = [
                ([_('day'), _('days')], 24 * 3600),
                ([_('hour'), _('hours')], 3600),
                ([_('minute'), _('minutes')], 60),
                ([_('second'), _('seconds')], 1)
            ]

            for unit_name, limit in unit_limits:
                if seconds >= limit:
                    amount = int(float(seconds) / limit)
                    if amount > 1:
                        unit_totals.append((unit_name[1], amount))
                    else:
                        unit_totals.append((unit_name[0], amount))
                    seconds = seconds - (amount * limit)
            unit_totals.append((_('seconds'), 0))

            return unit_totals

        active_phase = self.active_phase_ends_next
        if active_phase:
            today = timezone.now()
            time_delta = active_phase.end_date - today
            seconds = time_delta.total_seconds()
            time_delta_list = seconds_in_units(seconds)
            best_unit = time_delta_list[0]
            time_delta_str = '{} {}'.format(str(best_unit[1]),
                                            str(best_unit[0]))
            return time_delta_str

    @cached_property
    def active_phase_progress(self):
        """
        Return the progress of the currently active phase that ends next
        in percent.

        Attention: _deprecated_ as in the projects logic from the modules
        should be used.
        """
        warnings.warn(
            "active_phase_progress is deprecated as in the projects "
            "logic from the modules should be used; "
            "use module_running_progress",
            DeprecationWarning
        )
        active_phase = self.active_phase_ends_next
        if active_phase:
            time_gone = timezone.now() - active_phase.start_date
            total_time = active_phase.end_date - active_phase.start_date
            return round(time_gone / total_time * 100)
        return None
