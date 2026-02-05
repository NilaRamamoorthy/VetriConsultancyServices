from django.db import models

class ChatbotFAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    keywords = models.TextField(help_text="Comma separated keywords")

    def __str__(self):
        return self.question
