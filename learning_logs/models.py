from io import open_code
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    """A topic the user is learning about."""
    name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)

    def __str__(self):
        """Return a string representation of the model."""
        return self.name

class Entry(models.Model):
    """Something specific learned about a topic."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Return a string representation of the model."""
        string_representation = f"{self.text[:50]}"
        
        if(len(self.text) > 50):
            string_representation += "..."
        
        return f"{string_representation}"

class Comment(models.Model):
    """An opinion or a question expressed by a different user."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'comments'

    def __str__(self):
        """Return a string representation of the model."""

        string_representation = f"{self.text[:50]}"
        
        if(len(self.text) > 50):
            string_representation += "..."
        
        return f"{string_representation}"