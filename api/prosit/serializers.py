from api.prosit.models import (Semester, Prosit, PrositGroup, PrositStudent, PrositRole,)
from rest_framework import serializers


class SemesterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Semester
        fields = ["id", "title", "description"]
        read_only_field = ["id"]

class PrositSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prosit
        fields = ["id", "title", "data", "active", "achieved", "semester"]
        read_only_field = ["id"]

class PrositGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrositGroup
        fields = ["id", "title", "semester"]
        read_only_field = ["id"]

class PrositStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrositStudent
        fields = ["id", "prositGroup", "student"]
        read_only_field = ["id"]

class PrositRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrositRole
        fields = ["id", "prosit","prositGroup", "animator", "secretary", "timeKeeper", "scribe"]
        read_only_field = ["id"]

