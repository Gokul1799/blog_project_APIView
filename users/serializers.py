from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields='__all__'



# User Serializer
class UserSerializer(serializers.ModelSerializer):
    posts=serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    comments=serializers.PrimaryKeyRelatedField(many=True,read_only=True)

    class Meta:
        model=User
        fields=['id','username','email','posts','comments',]

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True},'style': {'input_type': 'password'}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user