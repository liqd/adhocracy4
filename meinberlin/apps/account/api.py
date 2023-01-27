from rest_framework import permissions
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response


class EndSessionView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        request.session.flush()
        return Response(status=status.HTTP_200_OK)
