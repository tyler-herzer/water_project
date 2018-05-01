import matplotlib.pyplot as plt
import numpy as np

import water_functions as wf

class WaterGraph():
	def __init__(self, settings):
		# Initialize important variables:
		self.settings = settings

		# Creating ideal values:
		self.x1 = [x for x in range(0, self.settings.day_hours + 1)]
		self.y1 = np.linspace(
			self.settings.morning_intake,
			self.settings.actual_daily_intake_, 
			self.settings.day_hours + 1)

		# Creating actual values:
		self.x2 = []
		self.y2 = []
		
		self.ax1 = plt.subplot2grid((1, 1,), (0, 0))

	def configure_graph(self):
		# Subplot style:
		for label in self.ax1.xaxis.get_ticklabels():
			label.set_rotation(45)
		self.ax1.xaxis.label.set_color('k')
		self.ax1.yaxis.label.set_color('k')
		self.ax1.set_xticks(self.x1)
		self.ax1.set_yticks(np.linspace(
			0,
			self.settings.actual_daily_intake_, 
			self.settings.day_hours + 1))

		# Graph style:
		plt.grid(True)#, color='g', linestyle='-', linewidth=1)
		plt.xlabel('Time')
		plt.ylabel('mL Water')
		plt.title('Daily Ideal Water Consumption')
		plt.subplots_adjust(left=0.12, bottom=0.18, right=0.90, top=0.88, wspace=0.2,
			hspace=0.2)
		wf.gen_x_labels(self.ax1, self.settings)
		plt.gcf().set_size_inches(10, 8)
		
	def show_graph(self):
		# Graph data:
		self.ax1.plot(self.x1, self.y1, label='Ideal', linewidth=2, color='c')
		self.ax1.plot(self.x2, self.y2, label='Actual', linewidth=2, color='orange')
		plt.legend()
		
		# Display graph:
		plt.show()
		
	def update_data(self, new_settings):
		# Updates the graph with most recently data before displaying it:
		data = wf.load_data()
		
		# Updated actual values:
		self.x2 = data['x2']
		self.y2 = data['y2']
		
		# Updated ideal values:
		self.x1 = [x for x in range(0, new_settings.day_hours + 1)]
		self.y1 = np.linspace(
			new_settings.morning_intake,
			new_settings.actual_daily_intake_, 
			new_settings.day_hours + 1)
			
		# Updated Subplot style:	
		self.ax1.set_yticks(np.linspace(
			0,
			self.settings.actual_daily_intake_, 
			self.settings.day_hours + 1))
			
		# Updated graph style:
		wf.gen_x_labels(self.ax1, new_settings)
