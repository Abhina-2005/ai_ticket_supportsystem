from django.shortcuts import render,get_object_or_404
from rest_framework.generics import CreateAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView,RetrieveUpdateAPIView,UpdateAPIView,RetrieveAPIView,DestroyAPIView
from rest_framework import authentication,permissions,filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from ticketassist.serializer import AdminSerializer,TicketSerializer,TicketCommentSerializer,UserSerializer,TicketAssignSerializer,AIAnalysisSerializer
from ticketassist.models import User,Ticket,TicketComment,AIAnalysis
from ticketassist.permissions import IsOwnerOrStaff,IsCommentOwnerOrStaff
from ticketassist.ai_service import generate_ai_response,generate_ai_analysis

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
        if self.request.user.is_staff:
            queryset=Ticket.objects.filter(assigned_to=self.request.user)
        else:
            queryset= Ticket.objects.filter(created_by=self.request.user)
        category=self.request.query_params.get("category")

        priority=self.request.query_params.get("priority")
        status=self.request.query_params.get("status")
        if category:
            queryset=queryset.filter(category=category)
        if priority:
            queryset=queryset.filter(priority=priority)
        if status:
            queryset=queryset.filter(status=status)
        return queryset
    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

class TicketRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[IsOwnerOrStaff]
    serializer_class=TicketSerializer
    queryset=Ticket.objects.all()

class TicketAssignView(RetrieveUpdateAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAdminUser]
    serializer_class=TicketAssignSerializer
    queryset=Ticket.objects.all()

class TicketCommentsListCreateView(ListCreateAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[IsCommentOwnerOrStaff]
    serializer_class=TicketCommentSerializer
    def get_queryset(self):
        ticket_object=get_object_or_404(Ticket,id=self.kwargs.get("pk"))
        if self.request.user.is_superuser:
            return TicketComment.objects.filter(ticket=ticket_object)
        if self.request.user.is_staff:
            return TicketComment.objects.filter(ticket=ticket_object,ticket__assigned_to=self.request.user)
        return TicketComment.objects.filter(ticket=ticket_object,ticket__created_by=self.request.user)

    def perform_create(self, serializer):
        # print(self.kwargs)
        ticket_object=get_object_or_404(Ticket,id=self.kwargs.get("pk"))
        return serializer.save(user=self.request.user,ticket=ticket_object)

class TicketCommentRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[IsCommentOwnerOrStaff]
    serializer_class=TicketCommentSerializer
    queryset=TicketComment.objects.all()

class TicketStatusView(UpdateAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[IsOwnerOrStaff]
    serializer_class=TicketSerializer
    queryset=Ticket.objects.all()


class TicketPriorityView(UpdateAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[IsOwnerOrStaff]
    serializer_class=TicketSerializer
    queryset=Ticket.objects.all()

class ProfileView(RetrieveAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=UserSerializer
    def get_object(self):
        return self.request.user

class LogoutView(RetrieveAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request):
        Token.objects.filter(user=request.user).delete()
        return Response({"messsage":"Logout successful"})

class TicketAIResponseView(CreateAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[IsOwnerOrStaff]
    def post(self,request,pk):
        ticket=get_object_or_404(Ticket,id=pk)
        if not ticket.description.strip():
            return Response({"errors":"ticket description cannot be empty"})
        try:
            response=generate_ai_response(ticket)
            if not response:
                return response({"errors":"unable to generate a suggested response at this time"})
            return Response({"msg":"AI response generated successfully","ticket_id":ticket.id,"suggested_response":response})

        except Exception:
            return Response({"error":"unable to generate a suggested response at this time"})

class TicketAIAnalysisView(CreateAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[IsOwnerOrStaff]
    def post(self,request,pk):
        ticket=get_object_or_404(Ticket,id=pk)
        try:
            result=generate_ai_analysis(ticket)
            analysis,created=AIAnalysis.objects.update_or_create(ticket=ticket,defaults=
                {
                    "summary": result.summary,
                    "suggested_category": result.suggested_category,
                    "suggested_priority": result.suggested_priority,
                    "sentiment": result.sentiment,
                    "suggested_response": result.suggested_response,
                }
                )
            return Response({"message":"AI analysis generated successfully ","analysis":AIAnalysisSerializer(analysis).data})
        except Exception :
            return Response({"errors":"unable to generate AI analysis at this time"}) 

class TicketAIAnalysisRetrieveView(RetrieveAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[IsOwnerOrStaff]
    serializer_class=AIAnalysisSerializer

    def get_object(self):
        ticket=get_object_or_404(Ticket,id=self.kwargs["pk"])
        return get_object_or_404(AIAnalysis,ticket=ticket)
          

   

    
    



        
    



        
