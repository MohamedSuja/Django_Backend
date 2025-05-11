from rest_framework import serializers

class SearchPropertyRequestSerializer(serializers.Serializer):
    page=serializers.IntegerField(default=1)
    page_size=serializers.IntegerField(default=10)
    data=serializers.DictField()