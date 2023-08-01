from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password1', 'access', 'refresh']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'email': {
                'write_only': True
            },
            'username': {
                'write_only': True
            },

        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['password'] != attrs['password1']:
            raise serializers.ValidationError({
                'password': 'both passwords do not match',
                'password1': 'both passwords do not match'
            })
        attrs.pop('password1')
        return attrs

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)

    def to_representation(self, instance):
        return instance.get_tokens()
