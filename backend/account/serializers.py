from rest_framework import serializers
from .models import CustomUser, Case, Mediator, Lawyer

class loginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=CustomUser
        fields=['email','password']


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class CaseSerializer(serializers.ModelSerializer):
    clients = CustomUserSerializer(many=True)
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

class MediatorSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    cases = CaseSerializer(many=True, read_only=True)
    history = CaseSerializer(many=True, read_only=True)

    class Meta:
        model = Mediator
        fields = ['user', 'rating', 'cases', 'history']

class LawyerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    current_cases = CaseSerializer(many=True, read_only=True)

    class Meta:
        model = Lawyer
        fields = ['user', 'docs', 'current_cases']
