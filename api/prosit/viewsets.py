from api.prosit.serializers import (SemesterSerializer, PrositGroupSerializer, PrositStudentSerializer,PrositSerializer,PrositRoleSerializer)
from api.prosit.models import (Semester, Prosit, PrositGroup, PrositStudent, PrositRole,)
from api.user.serializers import (UserSerializer)
from api.user.models import User
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import mixins


class SemesterViewSet(viewsets.GenericViewSet,  mixins.CreateModelMixin, mixins.UpdateModelMixin):
    serializer_class = SemesterSerializer
    error_message = {"success": False, "msg": "Error updating Semester"}

    def get(self, request):
        semesters = self.get_serializer(data=Semester.objects.all())
        

        return Response({
            "success": True,
            "semesters": semesters
            }, status.HTTP_200_OK)
        

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = Semester.objects.get(id=request.data.get("semesterID"))
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        user_id = request.data.get("userID")

        if not user_id:
            raise ValidationError(self.error_message)

        if self.request.user.pk != int(user_id) and (not self.request.user.is_superuser or not self.request.user.is_staff) :
            raise ValidationError(self.error_message)

        self.update(request)

        return Response({"success": True}, status.HTTP_200_OK)
    