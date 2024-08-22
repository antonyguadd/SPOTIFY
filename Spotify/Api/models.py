from django.db import models

class Token(models.Model):
    user = models.CharField(unique=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    access_token = models.TextField(max_length=500)  # Corregido el nombre del campo
    refresh_token = models.TextField(max_length=500)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)
