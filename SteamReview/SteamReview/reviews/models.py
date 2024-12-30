from django.db import models
from django.contrib.auth.models import User

#Making review class
class Review(models.Model):
    #Everthing that this class includes
    app_id = models.CharField(max_length=100)
    app_name = models.CharField(max_length=100, blank=True, null=True)
    app_developers = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    review_text = models.TextField()
    rating = models.CharField(max_length=10, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.app_id} - {self.review_text} by {self.user.username}"
