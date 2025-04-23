from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    recurrence = models.CharField(
        max_length=50,
        choices=[('None', 'None'), ('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly')],
        default='None'
    )

    def __str__(self):
        return self.name

class Invitation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    invitee = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)  # For SMS invites

    def __str__(self):
        return f"Invitation to {self.invitee} for {self.event.name}"

class Post(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    post_text = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post for {self.event.name}"

class Notification(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notified_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} about post {self.post.id}"

class RSVP(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.CharField(max_length=10, choices=[('Accepted', 'Accepted'), ('Declined', 'Declined')])

    def __str__(self):
        return f"{self.user.username} - {self.event.name} ({self.response})"

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

# Extra feature: Friend relationship for mutual contacts
class Friend(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend_of', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return f"{self.user.username} is friends with {self.friend.username}"
