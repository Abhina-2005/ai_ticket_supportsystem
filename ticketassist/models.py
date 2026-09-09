from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone=models.CharField(max_length=15,unique=True)

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
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


