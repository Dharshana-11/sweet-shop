from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    # Serialize the default User model with username and password
    class Meta:
        model = User
        fields = ['username', 'password'] 
    
    # Create a new user using the dafault function (includes password hashing)
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        
        return user
    
class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username = data["username"],
            password = data["password"]
        )

        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        data["user"] = user
        return data