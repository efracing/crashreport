from rest_framework import serializers


class ImageGroupSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    notes = serializers.CharField(allow_blank=True, allow_null=True)
    images = serializers.ListSerializer(child=serializers.CharField())


class CrashReportSerializer(serializers.Serializer):
    event = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    driver = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    date = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    porsche = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    sign = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    image_groups = ImageGroupSerializer(many=True)
