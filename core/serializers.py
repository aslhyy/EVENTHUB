from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(
        choices=[('attendee', 'Attendee'), ('organizer', 'Organizer')],
        default='attendee'
    )

    class Meta:
        model = User
        fields = ("username", "email", "password", "role")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
