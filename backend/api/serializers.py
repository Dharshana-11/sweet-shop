from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterUserSerializer(serializers.ModelSerializer):
    # Serialize the default User model with username and password
    class Meta:
        model = User
        fields = ['username', 'password'] 
    
    # Create a new user using the dafault function (includes password hashing)
    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            password = validated_data['password']
        )
        
        return user