from django.db import models

# The model for goals, includes all the aspects of the goal
# being tracked. Probably still needs to be normalized to scale well
class Goal(models.Model):
	ACTIVITY_CHOICES = (('Walking', 'Walking'), ('Running', 'Running'), ('Biking', 'Biking'),)
	TIME_FORMAT_CHOICES = (('MN', 'Minutes'), ('HR', 'Hours'),)
	person = models.ForeignKey('auth.User')
	goal_time = models.DecimalField(max_digits=5, decimal_places=2)
	time_worked_out = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	startDate = models.DateField(auto_now_add=True)
	finishDate = models.DateField() # might want to to constrain to weekly choices
	activity_type = models.CharField(max_length=7, choices=ACTIVITY_CHOICES)
	time_measured_in = models.CharField(max_length=2, choices=TIME_FORMAT_CHOICES)
	achieved = models.BooleanField(default=False)

	#calculates percentage of goal met
	def _get_progress(self):
		return round((self.time_worked_out / self.goal_time) * 100)
	progress = property(_get_progress)
	
class Contact(models.Model):
	person = models.ForeignKey('auth.User')
	number = models.DecimalField(max_digits=10, decimal_places=0)

def __str__(self):
	return (self.activity_type + " by " + self.finishDate)