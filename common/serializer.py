from rest_framework import serializers


class OperationError(serializers.Serializer):
    title = serializers.CharField()
    message = serializers.CharField()


class OperationSuccess(OperationError):
    data = serializers.JSONField(default={})
