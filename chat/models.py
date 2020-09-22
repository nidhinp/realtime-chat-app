from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Message(models.Model):
    text = models.TextField()
    room = models.ForeignKey(
        Room, related_name='messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
