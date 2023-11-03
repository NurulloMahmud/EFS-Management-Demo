from rest_framework import serializers

from main.models import (
    Efs,
    Used,
    StatusChange,
    Message,
    Department,
    UserDepartment
)


class EFSSerializer(serializers.ModelSerializer):
    class Meta:
        model = Efs
        fields = '__all__'