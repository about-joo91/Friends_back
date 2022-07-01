from rest_framework.views import APIView

from . import Google

class EmailSendView(APIView):
    def post(self, request):
        Google.create_service()
        