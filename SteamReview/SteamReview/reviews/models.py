from django.db import models

class Review(models.Model):
    app_id = models.CharField(max_length=100)
    review_text = models.TextField()
    # rating = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.app_id} - {self.review_text}"
