from rest_framework import serializers
from ticketassist.models import User,Ticket,TicketComment,AIAnalysis

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username","phone","email","password"]
        read_only_fields=["id"]
    def create(self, validated_data):
        return User.objects.create_superuser(**validated_data)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username","phone","email","password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ticket
        fields="__all__"
        read_only_fields=["id","created_by","assigned_to","created_at","updated_at"]

    def validate_title(self,value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty")
        return value
    def validate_description(self,value):
        if len(value.strip())<5:
            raise serializers.ValidationError("description must contain meaningful text")
        return value
    def validate_priority(self, value):
        valid_priorities=["low","medium","high","urgent"]
        if value not in valid_priorities:
            raise serializers.ValidationError("priority must be low,medium,high or urgent")
        return value

class TicketAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ticket
        fields=["assigned_to"]

class TicketCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=TicketComment
        fields="__all__"
        read_only_fields=["id","created_at","user","ticket"]

    def validate_title(self,value):
        if not value.strip():
            raise serializers.ValidationError("Title cananot be empty")
        return value
    def validate_description(self,value):
        if len(value.strip())<5:
            raise serializers.ValidationError("description must contain meaningful text")
        return value
    def validate_priority(self, value):
        valid_priorities=["low","medium","high","urgent"]
        if value not in valid_priorities:
            raise serializers.ValidationError("priority must be low,medium,high or urgent")
        return value

class AIAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
            model=AIAnalysis
            fields="__all__"
            read_only_fields=["id","ticket","summary","suggested_category","suggested_priority","sentiment","suggested_response","created_at"]
        
