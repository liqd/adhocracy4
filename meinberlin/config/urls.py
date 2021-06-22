"""meinberlin URL Configuration."""

from ckeditor_uploader import views as ck_views
from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog
from rest_framework import routers
from wagtail.contrib.sitemaps import views as wagtail_sitemap_views
from wagtail.contrib.sitemaps.sitemap_generator import \
    Sitemap as WagtailSitemap

from adhocracy4.api import routers as a4routers
from adhocracy4.comments.api import CommentViewSet
from adhocracy4.follows.api import FollowViewSet
from adhocracy4.polls.api import PollViewSet
from adhocracy4.polls.api import VoteViewSet
from adhocracy4.polls.routers import QuestionDefaultRouter
from adhocracy4.ratings.api import RatingViewSet
from adhocracy4.reports.api import ReportViewSet
from meinberlin.apps.bplan.api import BplanViewSet
from meinberlin.apps.contrib import views as contrib_views
from meinberlin.apps.contrib.sitemaps.adhocracy4_sitemap import \
    Adhocracy4Sitemap
from meinberlin.apps.contrib.sitemaps.static_sitemap import StaticSitemap
from meinberlin.apps.documents.api import DocumentViewSet
from meinberlin.apps.extprojects.api import ExternalProjectListViewSet
from meinberlin.apps.likes.api import LikesViewSet
from meinberlin.apps.likes.routers import LikesDefaultRouter
from meinberlin.apps.livequestions.api import LiveQuestionViewSet
from meinberlin.apps.moderatorremark.api import ModeratorRemarkViewSet
from meinberlin.apps.plans.api import PlansListViewSet
from meinberlin.apps.projectcontainers.api import ProjectContainerListViewSet
from meinberlin.apps.projects.api import PrivateProjectListViewSet
from meinberlin.apps.projects.api import ProjectListViewSet
from meinberlin.apps.users.decorators import user_is_project_admin

js_info_dict = {
    'packages': ('adhocracy4.comments',),
}

router = routers.DefaultRouter()
router.register(r'follows', FollowViewSet, basename='follows')
router.register(r'reports', ReportViewSet, basename='reports')
router.register(r'polls', PollViewSet, basename='polls')
router.register(r'projects', ProjectListViewSet, basename='projects')
router.register(r'privateprojects', PrivateProjectListViewSet,
                basename='privateprojects')
router.register(r'plans', PlansListViewSet, basename='plans')
router.register(r'extprojects',
                ExternalProjectListViewSet, basename='extprojects')
router.register(r'containers',
                ProjectContainerListViewSet, basename='containers')

module_router = a4routers.ModuleDefaultRouter()
# FIXME: rename to 'chapters'
module_router.register(r'documents', DocumentViewSet, basename='chapters')
module_router.register(r'questions', LiveQuestionViewSet, basename='questions')

likes_router = LikesDefaultRouter()
likes_router.register(r'likes', LikesViewSet, basename='likes')

orga_router = a4routers.OrganisationDefaultRouter()
orga_router.register(r'bplan', BplanViewSet, basename='bplan')

ct_router = a4routers.ContentTypeDefaultRouter()
ct_router.register(r'comments', CommentViewSet, basename='comments')
ct_router.register(r'ratings', RatingViewSet, basename='ratings')
ct_router.register(r'moderatorremarks', ModeratorRemarkViewSet,
                   basename='moderatorremarks')

question_router = QuestionDefaultRouter()
question_router.register(r'vote', VoteViewSet, basename='vote')

sitemaps = {
    'adhocracy4': Adhocracy4Sitemap,
    'wagtail': WagtailSitemap,
    'static': StaticSitemap
}

urlpatterns = [
    url(r'^django-admin/', admin.site.urls),
    url(r'^dashboard/', include('meinberlin.apps.dashboard.urls')),
    url(r'^account/', include('meinberlin.apps.account.urls')),
    url(r'^embed/', include('meinberlin.apps.embed.urls')),
    url(r'^initiators/', include(('meinberlin.apps.initiators.urls',
                                  'meinberlin_initiators'),
                                 'meinberlin_initiators')),

    url(r'^admin/', include('wagtail.admin.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^documents/', include('wagtail.documents.urls')),
    url(r'^projekte/', include('meinberlin.apps.projects.urls')),

    url(r'^ideas/', include(('meinberlin.apps.ideas.urls',
                             'meinberlin_ideas'),
                            'meinberlin_ideas')),
    url(r'^kiezkasse/', include(('meinberlin.apps.kiezkasse.urls',
                                 'meinberlin_kiezkasse'),
                                'meinberlin_kiezkasse')),
    url(r'^mapideas/', include(('meinberlin.apps.mapideas.urls',
                                'meinberlin_mapideas'),
                               'meinberlin_mapideas')),
    url(r'^text/', include(('meinberlin.apps.documents.urls',
                            'meinberlin_documents'),
                           'meinberlin_documents')),
    url(r'^bplan/', include(('meinberlin.apps.bplan.urls',
                             'meinberlin_bplan'),
                            'meinberlin_bplan')),
    url(r'^budgeting/', include(('meinberlin.apps.budgeting.urls',
                                 'meinberlin_budgeting'),
                                'meinberlin_budgeting')),
    url(r'^topicprio/', include(('meinberlin.apps.topicprio.urls',
                                 'meinberlin_topicprio'),
                                'meinberlin_topicprio')),
    url(r'^maptopicprio/', include(('meinberlin.apps.maptopicprio.urls',
                                    'meinberlin_maptopicprio'),
                                   'meinberlin_maptopicprio')),
    url(r'^offlineevents/', include(('meinberlin.apps.offlineevents.urls',
                                     'meinberlin_offlineevents'),
                                    'meinberlin_offlineevents')),
    url(r'^platform-emails/', include(('meinberlin.apps.platformemails.urls',
                                       'meinberlin_platformemails'),
                                      'meinberlin_platformemails')),
    url(r'^questions/', include(('meinberlin.apps.livequestions.urls',
                                 'meinberlin_livequestions'),
                                'meinberlin_livequestions')),
    url(r'', include(('meinberlin.apps.plans.urls',
                      'meinberlin_plans'),
                     'meinberlin_plans')),

    url(r'^api/', include(ct_router.urls)),
    url(r'^api/', include(likes_router.urls)),
    url(r'^api/', include(module_router.urls)),
    url(r'^api/', include(orga_router.urls)),
    url(r'^api/', include(question_router.urls)),
    url(r'^api/', include(router.urls)),

    url(r'^upload/',
        user_is_project_admin(ck_views.upload), name='ckeditor_upload'),
    url(r'^browse/', never_cache(user_is_project_admin(ck_views.browse)),
        name='ckeditor_browse'),

    url(r'^sitemap\.xml$', wagtail_sitemap_views.index,
        {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemaps'}),
    url(r'^sitemap-(?P<section>.+)\.xml$', wagtail_sitemap_views.sitemap,
        {'sitemaps': sitemaps}, name='sitemaps'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt',
        content_type="text/plain"), name="robots_file"),

    url(r'^components/$', contrib_views.ComponentLibraryView.as_view()),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'', include('wagtail.core.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media locally
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    try:
        import debug_toolbar
    except ImportError:
        pass
    else:
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
