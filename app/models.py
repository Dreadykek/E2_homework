from django.db import models

class Massage(models.Model):
    text = models.TextField(max_length=513)
    from_email = models.TextField(max_length=255)
    to_email = models.TextField(max_length=255)
    status = models.IntegerField(choices=[(0,'Not sended'), (1, 'Sended')], default=0)
