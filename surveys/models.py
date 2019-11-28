from django.db import models

class Survey(models.Model):
    id = models.AutoField(primary_key=True)
    survey_name = models.CharField(max_length=150)
    available_places = models.IntegerField()
    user_id = models.IntegerField()

class SurveyResponse(models.Model):
    id = models.AutoField(primary_key=True)
    survey_id = models.IntegerField()
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
