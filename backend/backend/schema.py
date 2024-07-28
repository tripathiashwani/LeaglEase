from account.models import CustomUser,Case,Mediator,Lawyer


import graphene
from graphene_django.types import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser

class CaseType(DjangoObjectType):
    class Meta:
        model = Case

class MediatorType(DjangoObjectType):
    class Meta:
        model = Mediator


class LawyerType(DjangoObjectType):
    class Meta:
        model = Lawyer




class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    cases = graphene.List(CaseType)
    mediators = graphene.List(MediatorType)
    lawyers = graphene.List(LawyerType)

    case = graphene.Field(CaseType, id=graphene.UUID())


    def resolve_users(self, info):
        return CustomUser.objects.all()

    def resolve_cases(self, info):
        return Case.objects.all()

    def resolve_mediators(self, info):
        return Mediator.objects.all()

    def resolve_lawyers(self, info):
        return Lawyer.objects.all()

    def resolve_case(self, info, id):
        return Case.objects.get(pk=id)
    
    
schema = graphene.Schema(query=Query)