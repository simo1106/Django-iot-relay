from django.db import models


class RelayState(models.Model):
    relay1 = models.CharField(max_length=10, default="off")
    relay2 = models.CharField(max_length=10, default="off")
    relay3 = models.CharField(max_length=10, default="off")
    relay4 = models.CharField(max_length=10, default="off")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"R1:{self.relay1}, R2:{self.relay2}, R3:{self.relay3}, R4:{self.relay4}"


class RelayLog(models.Model):
    SOURCE_CHOICES = [
        ("web", "Web"),
        ("mqtt", "MQTT"),
    ]

    relay1 = models.CharField(max_length=10)
    relay2 = models.CharField(max_length=10)
    relay3 = models.CharField(max_length=10)
    relay4 = models.CharField(max_length=10)
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES)
    topic = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.source} - {self.created_at}"