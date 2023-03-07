from rest_framework import filters


class StatusFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        now = view.now

        if "status" in request.GET:
            statustype = request.GET["status"]

            active_projects = queryset.filter(
                module__phase__start_date__lte=now,
                module__phase__end_date__gt=now,
                module__is_draft=False,
            ).distinct()

            future_projects = (
                queryset.filter(
                    module__phase__start_date__gt=now, module__is_draft=False
                )
                .distinct()
                .exclude(id__in=active_projects.values("id"))
            )

            if statustype == "activeParticipation":
                return active_projects

            if statustype == "futureParticipation":
                return future_projects

            if statustype == "pastParticipation":
                past_projects = (
                    queryset.filter(
                        module__phase__end_date__lt=now, module__is_draft=False
                    )
                    .distinct()
                    .exclude(id__in=active_projects.values("id"))
                    .exclude(id__in=future_projects.values("id"))
                )
                return past_projects

        return queryset
