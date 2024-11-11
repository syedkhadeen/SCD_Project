from rest_framework import serializers

class CalculationSerializer(serializers.Serializer):
    budget = serializers.FloatField()
    house_size = serializers.FloatField()
    sunlight = serializers.CharField()
    appliances = serializers.ListField(child=serializers.DictField())
