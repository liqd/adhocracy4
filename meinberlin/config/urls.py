"""meinberlin URL Configuration."""

from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import re_path
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog
from rest_framework import routers
from wagtail.contrib.sitemaps import views as wagtail_sitemap_views
from wagtail.contrib.sitemaps.sitemap_generator import Sitemap as WagtailSitemap

from adhocracy4.api import routers as a4routers
from adhocracy4.comments_async.api import CommentViewSet
from adhocracy4.follows.api import FollowViewSet
from adhocracy4.polls.api import PollViewSet
from adhocracy4.ratings.api import RatingViewSet
from adhocracy4.reports.api import ReportViewSet
from meinberlin.apps.bplan.api import BplanViewSet
from meinberlin.apps.budgeting.api import ProposalViewSet
from meinberlin.apps.contrib import views as contrib_views
from meinberlin.apps.contrib.sitemaps.adhocracy4_sitemap import Adhocracy4Sitemap
from meinberlin.apps.contrib.sitemaps.static_sitemap import StaticSitemap
from meinberlin.apps.documents.api import DocumentViewSet
from meinberlin.apps.extprojects.api import ExternalProjectListViewSet
from meinberlin.apps.likes.api import LikesViewSet
from meinberlin.apps.likes.routers import LikesDefaultRouter
from meinberlin.apps.livequestions.api import LiveQuestionViewSet
from meinberlin.apps.moderatorremark.api import ModeratorRemarkViewSet
from meinberlin.apps.plans.api import PlansListViewSet
from meinberlin.apps.projects.api import PrivateProjectListViewSet
from meinberlin.apps.projects.api import ProjectListViewSet
from meinberlin.apps.votes.api import TokenVoteViewSet
from meinberlin.apps.votes.routers import TokenVoteDefaultRouter

js_info_dict = {
    "packages": ("adhocracy4.comments",),
}

router = routers.DefaultRouter()
router.register(r"follows", FollowViewSet, basename="follows")
router.register(r"reports", ReportViewSet, basename="reports")
router.register(r"polls", PollViewSet, basename="polls")
router.register(r"projects", ProjectListViewSet, basename="projects")
router.register(
    r"privateprojects", PrivateProjectListViewSet, basename="privateprojects"
)
router.register(r"plans", PlansListViewSet, basename="plans")
router.register(r"extprojects", ExternalProjectListViewSet, basename="extprojects")

module_router = a4routers.ModuleDefaultRouter()
# FIXME: rename to 'chapters'
module_router.register(r"documents", DocumentViewSet, basename="chapters")
module_router.register(r"questions", LiveQuestionViewSet, basename="questions")
module_router.register(r"proposals", ProposalViewSet, basename="proposals")

likes_router = LikesDefaultRouter()
likes_router.register(r"likes", LikesViewSet, basename="likes")

orga_router = a4routers.OrganisationDefaultRouter()
orga_router.register(r"bplan", BplanViewSet, basename="bplan")

ct_router = a4routers.ContentTypeDefaultRouter()
ct_router.register(r"comments", CommentViewSet, basename="comments")
ct_router.register(r"ratings", RatingViewSet, basename="ratings")
ct_router.register(
    r"moderatorremarks", ModeratorRemarkViewSet, basename="moderatorremarks"
)

tokenvote_router = TokenVoteDefaultRouter()
tokenvote_router.register(r"tokenvotes", TokenVoteViewSet, basename="tokenvotes")

sitemaps = {
    "adhocracy4": Adhocracy4Sitemap,
    "wagtail": WagtailSitemap,
    "static": StaticSitemap,
}

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("dashboard/", include("meinberlin.apps.dashboard.urls")),
    path("account/", include("meinberlin.apps.account.urls")),
    path("embed/", include("meinberlin.apps.embed.urls")),
    path(
        "initiators/",
        include(
            ("meinberlin.apps.initiators.urls", "meinberlin_initiators"),
            "meinberlin_initiators",
        ),
    ),
    path("admin/", include("wagtail.admin.urls")),
    path("accounts/", include("allauth.urls")),
    path("documents/", include("wagtail.documents.urls")),
    path("projekte/", include("meinberlin.apps.projects.urls")),
    path(
        "ideas/",
        include(("meinberlin.apps.ideas.urls", "meinberlin_ideas"), "meinberlin_ideas"),
    ),
    path(
        "kiezkasse/",
        include(
            ("meinberlin.apps.kiezkasse.urls", "meinberlin_kiezkasse"),
            "meinberlin_kiezkasse",
        ),
    ),
    path(
        "mapideas/",
        include(
            ("meinberlin.apps.mapideas.urls", "meinberlin_mapideas"),
            "meinberlin_mapideas",
        ),
    ),
    path(
        "text/",
        include(
            ("meinberlin.apps.documents.urls", "meinberlin_documents"),
            "meinberlin_documents",
        ),
    ),
    path(
        "bplan/",
        include(("meinberlin.apps.bplan.urls", "meinberlin_bplan"), "meinberlin_bplan"),
    ),
    path(
        "budgeting/",
        include(
            ("meinberlin.apps.budgeting.urls", "meinberlin_budgeting"),
            "meinberlin_budgeting",
        ),
    ),
    path(
        "topicprio/",
        include(
            ("meinberlin.apps.topicprio.urls", "meinberlin_topicprio"),
            "meinberlin_topicprio",
        ),
    ),
    path(
        "maptopicprio/",
        include(
            ("meinberlin.apps.maptopicprio.urls", "meinberlin_maptopicprio"),
            "meinberlin_maptopicprio",
        ),
    ),
    path(
        "offlineevents/",
        include(
            ("meinberlin.apps.offlineevents.urls", "meinberlin_offlineevents"),
            "meinberlin_offlineevents",
        ),
    ),
    path(
        "platform-emails/",
        include(
            ("meinberlin.apps.platformemails.urls", "meinberlin_platformemails"),
            "meinberlin_platformemails",
        ),
    ),
    path(
        "questions/",
        include(
            ("meinberlin.apps.livequestions.urls", "meinberlin_livequestions"),
            "meinberlin_livequestions",
        ),
    ),
    path(
        "",
        include(("meinberlin.apps.plans.urls", "meinberlin_plans"), "meinberlin_plans"),
    ),
    path("api/", include(ct_router.urls)),
    path("api/", include(likes_router.urls)),
    path("api/", include(module_router.urls)),
    path("api/", include(orga_router.urls)),
    path("api/", include(tokenvote_router.urls)),
    path("api/", include(router.urls)),
    path(
        "ckeditor5/", include("django_ckeditor_5.urls"), name="ck_editor_5_upload_file"
    ),
    path(
        "sitemap.xml",
        wagtail_sitemap_views.index,
        {"sitemaps": sitemaps, "sitemap_url_name": "sitemaps"},
    ),
    re_path(
        r"^sitemap-(?P<section>.+)\.xml$",
        wagtail_sitemap_views.sitemap,
        {"sitemaps": sitemaps},
        name="sitemaps",
    ),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots_file",
    ),
    path("components/", contrib_views.ComponentLibraryView.as_view()),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("", include("wagtail.urls")),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media locally
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    try:
        import debug_toolbar
    except ImportError:
        pass
    else:
        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
        ] + urlpatterns
