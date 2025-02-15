from datetime import datetime
from django import test
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator
from datetime import datetime

# Resolves test 5
def validate_stroke(test_stroke):
    valid_strokes = ['front crawl', 'butterfly', 'breast', 'back', 'freestyle']
    if test_stroke not in valid_strokes:
        raise ValidationError(f"{test_stroke} is not a valid stroke")

# Resolves test 6
def validate_distance(distance):
    if distance < 50:
        raise ValidationError(f"Ensure this value is greater than or equal to 50.")

# Resolves test 7
def validate_future_date(test_date):
    if test_date > timezone.now():
        raise ValidationError("Can't set record in the future.")


class SwimRecord(models.Model):
    # pass
    first_name = models.CharField(max_length=200, null=False)
    last_name = models.CharField(max_length=200, null=False)
    team_name = models.CharField(max_length=200, null=False)
    relay = models.BooleanField(null=False)
    stroke = models.CharField(max_length=200, null=False, validators=[validate_stroke])
    distance = models.IntegerField(validators=[validate_distance])
    record_date = models.DateTimeField(validators=[validate_future_date])
    record_broken_date = models.DateTimeField()


    # Use a self comparison that fires when the model.save() is called
    # Record broken validator
    def clean(self):
        cleaned_data = super().clean()
        if self.record_date and self.record_broken_date:
            if self.record_date >= self.record_broken_date:
                raise ValidationError({'record_broken_date':"Can't break record before record was set."})
