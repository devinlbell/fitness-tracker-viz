from django.forms import widgets
from rest_framework import serializers
from .models import Goal

class GoalSerializer(serializers.ModelSerializer): 
	class Meta:
		model = Goal
		fields = ('time_worked_out', 'goal_time', 'time_measured_in','activity_type', 'finishDate', 'startDate', 'finishDate', 'person')