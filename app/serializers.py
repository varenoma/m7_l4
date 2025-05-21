from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from rest_framework import serializers
from django.urls import reverse

from .models import QatagonlarClassModel

from datetime import datetime


class QatagonlarSerializers(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = QatagonlarClassModel
        fields = ('full_name', 'birth_year', 'slug', 'detail_url')

    def validate_birth_year(self, value):
        hozirgi_yil = datetime.now().date()
        if value > hozirgi_yil:
            raise serializers.ValidationError(
                f"{value.year} yil hali kelmagan — hozirgi yildan keyin bo'lishi mumkin emas")
        return value

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(
            reverse('list-detail', kwargs={'slug': obj.slug}))


class QatagonlarDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = QatagonlarClassModel
        fields = ('full_name', 'bio', 'birth_year', 'died_year')

    def validate_birth_year(self, value):
        hozirgi_yil = datetime.now().date()
        if value > hozirgi_yil:
            raise serializers.ValidationError(
                f"{value.year} yil hali kelmagan — hozirgi yildan keyin bo'lishi mumkin emas.")
        return value


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
