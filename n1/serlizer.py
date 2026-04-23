from rest_framework import serializers
from .models import na


class naSerializer(serializers.ModelSerializer):
    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Name must be at least 3 characters long")
        return value

    class Meta:
        model = na
        fields = '__all__'


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = na
        fields = ["id", "name", ]


class UserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = na
        fields = ["name", "email", "password"]

    def create(self, validated_data):
        return na.objects.create(**validated_data)
