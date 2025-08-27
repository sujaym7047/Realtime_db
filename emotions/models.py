from django.db import models
    

class EmotionLog(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.CharField(max_length=100)
    emotion = models.CharField(max_length=50)
    class Meta:
        db_table="EmotionLog"