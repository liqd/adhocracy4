from django.apps import AppConfig


class Config(AppConfig):
    name = "meinberlin.apps.actions"
    label = "meinberlin_actions"

    def ready(self):
        from adhocracy4.actions.models import configure_icon
        from adhocracy4.actions.models import configure_type
        from adhocracy4.actions.verbs import Verbs

        configure_type(
            "project",
            ("a4projects", "project"),
            ("meinberlin_bplan", "bplan"),
            ("meinberlin_externalproject", "externalproject"),
        )
        configure_type("phase", ("a4phases", "phase"))
        configure_type("comment", ("a4comments", "comment"))
        configure_type("rating", ("a4ratings", "rating"))
        configure_type(
            "item",
            ("meinberlin_budgeting", "proposal"),
            ("meinberlin_ideas", "idea"),
            ("meinberlin_kiezkasse", "proposal"),
            ("meinberlin_mapideas", "mapidea"),
        )
        configure_type("offlineevent", ("meinberlin_offlineevents", "offlineevent"))

        configure_icon("far fa-comment", type="comment")
        configure_icon("far fa-lightbulb", type="item")
        configure_icon("fas fa-plus", verb=Verbs.ADD)
        configure_icon("fas fa-pencil-alt", verb=Verbs.UPDATE)
        configure_icon("fas fa-flag", verb=Verbs.START)
        configure_icon("far fa-clock", verb=Verbs.SCHEDULE)
