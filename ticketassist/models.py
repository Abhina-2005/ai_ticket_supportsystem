from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
# from ticketassist.models import User,profile

class User(AbstractUser):
    phone=models.CharField(max_length=15,unique=True)

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

class Ticket(models.Model):
    CATEGORY_CHOICES=(
        ("technical","technical"),
        ("payment","payment"),
        ("account","account"),
        ("delivery","delivery"),
        ("product","product"),
        ("other","other")
    )

    PRIORITY_CHOICES=(
        ("low","low"),
        ("high","high"),
        ("medium","medium"),
        ("urgent","urgent")
    )

    STATUS_CHOICES=(
        ("open","open"),
        ("in-progress","in-progress"),
        ("resolved","resolved"),
        ("closed","closed")
    )

    title=models.CharField(max_length=200,)
    description=models.TextField()
    category=models.CharField(max_length=50,choices=CATEGORY_CHOICES)
    priority=models.CharField(max_length=50,choices=PRIORITY_CHOICES)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default="open")
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name="tickets")
    assigned_to=models.ForeignKey(User,on_delete=models.CASCADE,related_name="assigned_tickets",null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TicketComment(models.Model):
    ticket=models.ForeignKey(Ticket,on_delete=models.CASCADE,related_name="comments")
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="ticket_comments")
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticket.title}-{self.user.username}"

class AIAnalysis(models.Model):
    SUGGESTED_CATEGORY_CHOICES=(
            ("technical","technical"),
            ("payment","payment"),
            ("account","account"),
            ("delivery","delivery"),
            ("product","product"),
            ("other","other")
        )
    
    SUGGESTED_PRIORITY_CHOICES=(
            ("low","low"),
            ("medium","medium"),
            ("high","high"),
            ("urgent","urgent")
        )

    SENTIMENT_CHOICES=(
            ("positive","positive"),
            ("neutral","neutral"),
            ("negative","negative")
        )
    
    ticket=models.OneToOneField(Ticket,on_delete=models.CASCADE,related_name="ai_analysis")
    summary=models.TextField()
    suggested_catrgory=models.CharField(max_length=50,choices=SUGGESTED_CATEGORY_CHOICES)
    suggested_priority=models.CharField(max_length=50,choices=SUGGESTED_PRIORITY_CHOICES)
    sentiment=models.CharField(max_length=50,choices=SENTIMENT_CHOICES)
    suggested_response=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI analysis -{self.ticket.title}"

from django.db.models.signals import post_save

def create_profile(sender,instance,created,**kwargs):
    if created and not instance.is_superuser and not instance.is_staff:
        Profile.objects.create(user=instance)
post_save.connect(create_profile,User)
        







