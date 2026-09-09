from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView,ListCreateAPIView
from rest_framework import authentication,permissions
from ticketassist.serializer import AdminSerializer,TicketSerializer
from ticketassist.models import User,Ticket

class SignupView(CreateAPIView):
    serializer_class=AdminSerializer

class TicketListCreateView(ListCreateAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAdminUser]
    serializer_class=TicketSerializer

    def get_queryset(self):
        return Ticket.objects.filter(created_by=self.request.user)
    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)
    
    
