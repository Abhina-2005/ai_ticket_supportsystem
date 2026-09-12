"""
URL configuration for helpdesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from ticketassist.views import SignupView
from ticketassist.views import UserSignUpView
from ticketassist.views import TicketListCreateView
from ticketassist.views import TicketRetrieveUpdateDeleteView
from ticketassist.views import TicketCommentsListCreateView
from ticketassist.views import TicketCommentRetrieveUpdateDeleteView
from ticketassist.views import TicketAssignView
from ticketassist.views import TicketStatusView
from ticketassist.views import TicketPriorityView
from ticketassist.views import ProfileView
from ticketassist.views import LogoutView
from ticketassist.views import TicketAIResponseView
from ticketassist.views import TicketAIAnalysisView
from ticketassist.views import TicketAIAnalysisRetrieveView


urlpatterns = [
    path('admin/',admin.site.urls),
    path("api/token/",ObtainAuthToken.as_view()),
    path("api/admin/register/",SignupView.as_view()),
    path("api/user/register/",UserSignUpView.as_view()),
    path("api/tickets/",TicketListCreateView.as_view()),
    path("api/tickets/<int:pk>/",TicketRetrieveUpdateDeleteView.as_view()),
    path("api/tickets/<int:pk>/comments/",TicketCommentsListCreateView.as_view()),
    path("api/tickets/<int:ticket_id>/comments/<int:pk>/",TicketCommentRetrieveUpdateDeleteView.as_view()),
    path("api/ticket/<int:pk>/assign/",TicketAssignView.as_view()),
    path("api/tickets/<int:pk>/status/",TicketStatusView.as_view()),
    path("api/tickets/<int:pk>/priority/",TicketPriorityView.as_view()),
    path("api/profile/",ProfileView.as_view()),
    path("api/logout/",LogoutView.as_view()),
    path("api/ticket/<int:pk>/ai-response/",TicketAIResponseView.as_view()),
    path("api/tickets/<int:pk>/ai-analysis/",TicketAIAnalysisView.as_view()),
    path("api/tickets/<int:pk>/ai-analysis/retrieve/",TicketAIAnalysisRetrieveView.as_view()),
]
