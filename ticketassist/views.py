from django.shortcuts import render,get_object_or_404
from rest_framework.generics import CreateAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework import authentication,permissions,filters
from ticketassist.serializer import AdminSerializer,TicketSerializer,TicketCommentSerializer,UserSerializer
from ticketassist.models import User,Ticket,TicketComment
# Create your views here.


class SignupView(CreateAPIView):
    serializer_class=AdminSerializer

class UserSignUpView(CreateAPIView):
    serializer_class=UserSerializer


class TicketListCreateView(ListCreateAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=TicketSerializer

    filter_backends=[filters.SearchFilter,filters.OrderingFilter]
    search_fields=["title","description"]
    ordering_fields=["created_at","updated_at","priority"]

    def get_queryset(self):
        queryset= Ticket.objects.filter(created_by=self.request.user)
        category=self.request.query_params.get("category")

        priority=self.request.query_params.get("priority")
        if category:
            queryset=queryset.filter(category=category)
        if priority:
            queryset=queryset.filter(priority=priority)
        return queryset
    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

class TicketRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=TicketSerializer
    queryset=Ticket.objects.all()

class TicketCommentsListCreateView(ListCreateAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=TicketCommentSerializer
    def get_queryset(self):
        ticket_object=get_object_or_404(Ticket,id=self.kwargs.get("pk"))
        return TicketComment.objects.filter(user=self.request.user,ticket=ticket_object)
    def perform_create(self, serializer):
        # print(self.kwargs)
        ticket_object=get_object_or_404(Ticket,id=self.kwargs.get("pk"))
        return serializer.save(user=self.request.user,ticket=ticket_object)
    



        
    



        
