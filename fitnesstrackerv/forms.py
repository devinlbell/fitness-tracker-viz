from django import forms
from .models import Goal, Contact


class GoalForm(forms.ModelForm):
	
	class Meta:
		model = Goal
		fields = ('goal_time', 'time_measured_in','activity_type', 'finishDate')

class UpdateForm(forms.ModelForm):
	class Meta:
		model = Goal
		fields = ('time_worked_out', 'goal_time', 'time_measured_in','activity_type', 'finishDate')

class ContactForm(forms.ModelForm):
	class Meta:
		model = Contact
		fields = ('number',)

		