from abc import ABC

from rest_framework import serializers

from apps.project.models import Report


class ReportSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=3000, allow_null=True, allow_blank=True)
    smeta = serializers.JSONField(allow_null=True)
    cost = serializers.JSONField(allow_null=True)
    result = serializers.JSONField(allow_null=True)

    def create(self, validated_data):
        return Report.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.smeta = validated_data.get('smeta', instance.smeta)
        instance.cost = validated_data.get('cost', instance.cost)
        instance.result = validated_data.get('result', instance.result)

        instance.save()
        return instance


class ReportEventSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=3000, allow_null=True, allow_blank=True)
    start_date = serializers.CharField(allow_null=True)
    finish_date = serializers.CharField(allow_null=True)
    result = serializers.CharField(allow_null=True)
    report = serializers.CharField(allow_null=True)
    id = serializers.CharField(allow_null=True)

    def update(self, instance, validated_data):
        instance.report = validated_data.get('report', instance.result)

        instance.save()
        return instance
