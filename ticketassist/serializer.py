from rest_framework import serializers
from ticketassist.models import User,Ticket

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username","phone","email","password"]
        read_only_fields=["id"]
    def create(self, validated_data):
        return User.objects.create_superuser(**validated_data)

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ticket
        fields="__all__"
        read_only_fields=["id","created_by","assigned_to","category","priority","status","created_at","updated_at"]