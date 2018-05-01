import time

class Settings():
	"""Settings for my water intake program."""
	def __init__(self):
		'''Attributes ending with _ are designated to not be adjusted via cmd
		commands.'''

		# Schedule Settings
		self.initial_time = "2:30pm" # Must be in "H:MMam" format.
		self.day_hours = 15

		# Water Settings
		self.ideal_daily_intake = 3700 # Daily intake based on 16 hour day.
		self.hourly_intake_ = (
			round(self.ideal_daily_intake / 16))
		self.actual_daily_intake_ = self.hourly_intake_ * self.day_hours
		self.morning_intake = 300 # Amount to drink immediately after waking.
		self.bottle_capacity = 1400 # Bottle size in mL
			
		# Reminder Settings
		self.reminder_interval = 15 * 60 # Minutes * 60 seconds (constant).
		self.reminder_default_config = {"alert_noise": True}
