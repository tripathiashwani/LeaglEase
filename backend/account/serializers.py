from rest_framework import serializers
from .models import CustomUser, Case, Mediator, Lawyer

class loginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=CustomUser
        fields=['email','password']


# serializers.py

# class UserSerializer(serializers.ModelSerializer):
#     password1 = serializers.CharField(write_only=True)
#     password2 = serializers.CharField(write_only=True)

#     class Meta:
#         model = CustomUser
#         fields = ['id', 'name', 'email', 'password1', 'password2']

#     def validate(self, data):
#         if data['password1'] != data['password2']:
#             raise serializers.ValidationError("Passwords do not match.")
#         return data

#     def create(self, validated_data):
#         validated_data.pop('password2')
#         password = validated_data.pop('password1')
#         user = CustomUser(**validated_data)
#         user.set_password(password)
#         user.save()
#         return user

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')
        user = CustomUser(email=validated_data['email'])
        user.set_password(password)
        user.save()
        return user

class MediatorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Mediator
        fields = ['user', 'rating', 'docs']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        mediator = Mediator.objects.create(user=user, **validated_data)
        return mediator


class CaseSerializer(serializers.ModelSerializer):
    clients = UserSerializer(many=True)
    mediator = serializers.SlugRelatedField(slug_field='user', queryset=Mediator.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Case
        fields = ['id', 'type_of_case', 'clients', 'mediator']

    def create(self, validated_data):
        clients_data = validated_data.pop('clients')
        case = Case.objects.create(**validated_data)
        for client_data in clients_data:
            user = CustomUser.objects.get(id=client_data['id'])
            case.clients.add(user)
        return case

    def update(self, instance, validated_data):
        clients_data = validated_data.pop('clients')
        instance.type_of_case = validated_data.get('type_of_case', instance.type_of_case)
        instance.mediator = validated_data.get('mediator', instance.mediator)
        instance.save()

        instance.clients.clear()
        for client_data in clients_data:
            user = CustomUser.objects.get(id=client_data['id'])
            instance.clients.add(user)

        return instance

# class MediatorSerializer(serializers.ModelSerializer):
#     user = UserSerializer()

#     class Meta:
#         model = Mediator
#         fields = ['user', 'rating', 'docs']

#     def create(self, validated_data):
#         password = validated_data.pop('password1')
#         user = CustomUser(**validated_data)  # Use create_user to create CustomUser
#         mediator = Mediator.objects.create(user=user, **validated_data)
#         return mediator

class LawyerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Lawyer
        fields = ['user', 'docs']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create_user(**user_data)
        lawyer = Lawyer.objects.create(user=user, **validated_data)
        return lawyer