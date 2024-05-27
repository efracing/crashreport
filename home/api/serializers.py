from rest_framework import serializers


class ImageSerializer(serializers.Serializer):
    image = serializers.CharField(allow_blank=True, allow_null=True)


class ImageGroupSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    notes = serializers.CharField(allow_blank=True, allow_null=True)
    images = ImageSerializer(many=True)


class CrashReportSerializer(serializers.Serializer):
    event = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    driver = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    date = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    porsche = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    sign = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    image_groups = ImageGroupSerializer(many=True)
