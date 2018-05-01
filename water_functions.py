import collections
import datetime
import json
import matplotlib.pyplot as plt
# import reminder (In begin_reminder())
import time
import winsound

from water_graph import WaterGraph
from water_settings import Settings

# Welcome message:
print('------------------------------')
print('Water Tracking successfully loaded!')
print('Enter wf.commands() to see a list of available commands')
print('------------------------------')

# Initialize important variables:
last_reminder_time = 0
graph_intersect_time = 0

# Initialize class instances:
settings = Settings()

# Core commands:
def mute_reminder(boolean):
	if boolean == False:
		enable_alert()
	elif boolean == True:
		disable_alert()
	else:
		print("alert() only accepts True or False")
	
def begin_day():
	delete_old_data()
	confirm_settings()
	initial_data = {
		'alarm_time': get_alarm_time(),
		'previous_update_time': "No previous updates!",
		'bottle_number': 1,
		'previous_measurement': get_morning_measurement(),
		'x2': [0],
		'y2': [0],
		}
	save_data(initial_data)
	
def begin_reminder():
	import reminder
	
def commands():
	print("\nwf.mute_reminder(): Takes True or False to silence/enable " + 
		"reminders.\n")
	print("wf.begin_day(): Deletes previous day's data and initializes data " +
		"needed for a \nnew day.\n")
	print("wf.begin_reminder(): Begins the reminder sound notifications at " +
		"an interval \nspecified via the water_settings.py file.\n")
	print("wf.display_graph(): Updates the graph data with all data from " +
		"current day \nthen displays it.\n")
	print("wf.refill(): Prompts an update for current water measurements as " +
		"well as an \namount to which the bottle will be refilled.\n")
	print("wf.revert_data(): Replaces the most recent data file with the " +
		"backup data \nfile.")
	print("wf.update(): Prompts an update for current water measurements so " +
		"that the data \nmay be stored and accessible via graph.\n")
	
def display_graph():
	water_graph = WaterGraph(settings)
	water_graph.configure_graph()
	water_graph.update_data(settings)
	water_graph.show_graph()
	
def refill():
	update(include_refill='True')
	
def revert_data():
	backup_data = load_data_backup()
	save_data(backup_data)

def update(include_refill=''):
	previous_data_file = load_data()
	display_previous_update_data(previous_data_file)
	backup_data_file(previous_data_file)
	current_data_file = get_current_update_data(previous_data_file,
		include_refill=include_refill)
	display_success()
	save_data(current_data_file)

# Core command helpers:
def backup_data_file(data_file):
	with open('json_files//data_backup.json', 'w') as f_obj:
		json.dump(data_file, f_obj)

def calc_time_since_alarm(data_file):
	current_time = time.time()
	alarm_time = data_file['alarm_time']
	time_since_alarm = ((current_time - alarm_time) / 60) / 60
	return time_since_alarm
	
def calc_water_quantities(current_bottle_num, prev_bottle_num, 
		prev_measurement):
	current_measurement = get_bottle_measurement()
	bottle_number_diff = current_bottle_num - prev_bottle_num
	quantity_drank = (
		prev_measurement - 
		current_measurement + 
		bottle_number_diff * 
		settings.bottle_capacity
		)
	WaterTuple = collections.namedtuple('WaterTuple', [
		'current_measurement', 'quantity_drank'])
	quantities = WaterTuple(current_measurement, quantity_drank)
	return quantities
	
def confirm_settings():
	display_settings()
	while True:
		print("Enter 'next' to exit settings adjustment menu")
		choice = input("Enter setting you wish to adjust: ")
		if choice == 'next':
			break
		value = input("Enter a new value for that setting: ")
		if value == 'next':
			break
		if type(getattr(settings, choice)) == str:
			setattr(settings, choice, value)
		else:
			value = int(value)
			setattr(settings, choice, value)
		display_settings()
	save_settings()

def delete_old_data():
	with open('json_files//data.json', 'w') as f_obj:
		json.dump({}, f_obj)

def disable_alert():
	config = load_config()
	config['alert_noise'] = False
	save_config(config)
	
def display_previous_update_data(data_file):
	print("------------------------------")
	print("Previous update details:\n")
	print("  Time: " + data_file['previous_update_time'])
	print("  Bottle Number: " + str(data_file['bottle_number']))
	print("  Previous Measurement: " + 
		str(data_file['previous_measurement']) + "mL")
	print("------------------------------")
	
def display_settings():
	print('')
	settings_dict = settings.__dict__
	i = 1
	for k, v in settings_dict.items():
		if not str(k).endswith('_'):
			print("{}.){} ".format(i, k) + ": " + str(v))
			i += 1
	print('')
	
def display_success():
	print("Data successfully updated!")

def enable_alert():
	config = load_config()
	config['alert_noise'] = True
	save_config(config)
	
def find_second_difference(alarm, current):
	difference = current - alarm
	if difference < 0:
		total_day_seconds = 24 * 60 * 60
		difference = (total_day_seconds - 
			alarm + current)
	return difference
	
	
def get_alarm_seconds():
	alarm_time = settings.initial_time
	alarm_colon_index = alarm_time.find(":")
	alarm_hour = alarm_time[:alarm_colon_index]
	if alarm_hour == "12":
		alarm_hour = 0
	alarm_minute = alarm_time[alarm_colon_index + 1:-2]
	alarm_total_minutes = (int(alarm_hour) * 60 + int(alarm_minute))
	alarm_total_seconds = alarm_total_minutes * 60
	if alarm_time.endswith("pm"):
		alarm_total_seconds += 12 * 60 * 60
	return alarm_total_seconds
	
def get_alarm_time():
	alarm_seconds = get_alarm_seconds()
	current_seconds = get_current_seconds()
	offset_seconds = find_second_difference(alarm_seconds, current_seconds)
	corrected_time = time.time() - offset_seconds
	return corrected_time
		
def get_bottle_measurement():
	measurement = int(input("Current bottle measurement: "))
	return measurement

def get_bottle_number():
	bottle_number = int(input("Current bottle number: "))
	return bottle_number
	
def get_current_seconds():
	current_time = str(datetime.datetime.now().time())
	hour_colon_index = current_time.find(":")
	current_hour = int(current_time[:hour_colon_index])
	
	minute_colon_relative = current_time[hour_colon_index + 1:].find(":")
	minute_colon_index = hour_colon_index + minute_colon_relative + 1
	current_minute = int(current_time[hour_colon_index + 1:minute_colon_index])
	
	current_total_minutes = current_hour * 60 + current_minute
	current_total_seconds = current_total_minutes * 60
	return current_total_seconds
	
def get_current_update_data(data_file, include_refill=''):
	current_bottle_num = get_bottle_number()
	prev_bottle_num = data_file['bottle_number']
	prev_measurement = data_file['previous_measurement']
	water_quantities = calc_water_quantities(current_bottle_num,
		prev_bottle_num, prev_measurement)
	time_since_alarm = calc_time_since_alarm(data_file)
	quantity_drank = water_quantities.quantity_drank
	previous_quantity_drank = data_file['y2'][-1]
		
	data_file['bottle_number'] = current_bottle_num
	data_file['previous_update_time'] = str(datetime.datetime.now().time())
	if include_refill:
		measurement_after_refill = get_refill_quantity()
		data_file['previous_measurement'] = measurement_after_refill
	else:
		data_file['previous_measurement'] = water_quantities.current_measurement
	data_file['x2'].append(round(time_since_alarm, 3))
	data_file['x2'].append(round(time_since_alarm, 3)) # x2
	data_file['y2'].append(previous_quantity_drank)
	data_file['y2'].append(previous_quantity_drank + quantity_drank) #y2
	return data_file
	
def get_morning_measurement():
	response = input("Bottle is full? (True/False) ")
	if response.title() == 'True':
		measurement = settings.bottle_capacity
	else:
		measurement = int(input("Current bottle measurement: "))
	return measurement
	
def get_refill_quantity():
	measurement_after_refill = int(input("Measurement after refilling: "))
	return measurement_after_refill

def load_config():
	with open('json_files//config.json', 'r') as f_obj:
		config = json.load(f_obj)
		return config
		
def load_data():
	with open('json_files//data.json', 'r') as f_obj:
		data = json.load(f_obj)
		return data
		
def load_data_backup():
	with open('json_files//data_backup.json', 'r') as f_obj:
		data = json.load(f_obj)
		return data
		
def load_settings():
	with open('json_files//settings.json', 'r') as f_obj:
		data = json.load(f_obj)
		return data
		
def save_config(config):
	with open('json_files//config.json', 'w') as f_obj:
		json.dump(config, f_obj)
		
def save_data(data_file):
	with open('json_files//data.json', 'w') as f_obj:
		json.dump(data_file, f_obj)
		
def save_settings():
	with open('json_files//settings.json', 'w') as f_obj:
		json.dump(settings.__dict__, f_obj)
	
def update_settings():
	settings_data = load_settings()
	for k, v in settings_data.items():
		setattr(settings, k, v)

# Graph style functions:
def gen_x_labels(axes, settings):
	text_labels = [label.get_text() for label in axes.get_xticklabels()]
	time = settings.initial_time
	for index_num in range(0, settings.day_hours + 1):
		text_labels[index_num] = time
		time = increment_time(time)
	
	axes.set_xticklabels(text_labels)
	
def increment_time(time):
	colon_index = time.find(":")
	old_hour = time[:colon_index]
	if old_hour != '12':	
		new_hour = int(old_hour) + 1
		new_time = time.replace(
		"{}".format(old_hour),
		"{}".format(new_hour),
		1)
		return new_time
	else:
		new_hour = 1
		new_time = time.replace(
		"{}".format(old_hour),
		"{}".format(new_hour),
		1)
		if new_time[-2:] == "am":
			new_time = new_time.replace("am", "pm")
		else:
			new_time = new_time.replace("pm", "am")
		return new_time
		
# Reminder functions
def check_reminder():
	update_graphs_intersect_time()
	display_reminder_info()
	if graphs_intersect():
		if time_interval_passed():
			reset_last_reminder_time()
			play_reminder()
			
def display_reminder_info():
	print('')
	print(get_amount_ahead())
	print(time_until_intersect())
	
def get_amount_ahead():
	data = load_data()
	alarm_time = data['alarm_time']
	current_time = time.time()
	seconds_since_alarm = current_time - alarm_time
	hours_since_alarm = (seconds_since_alarm / 60) / 60
	
	y2 = data['y2'][-1]
	y1 = ((hours_since_alarm * (
		(settings.actual_daily_intake_ - settings.morning_intake) /
		settings.day_hours)) + settings.morning_intake)
	amount_ahead = int(y2 - y1)
	amount_sign = "+" if amount_ahead > 0 else "-"
	return "Ideal consumption comparison: {}{}mL".format(amount_sign,
		abs(amount_ahead))
	
def graphs_intersect():
	current_time = time.time()
	if current_time > graph_intersect_time:
		return True
	else:
		return False
		
def initialize_config():
	with open('json_files//config.json', 'w') as f_obj:
		json.dump(settings.reminder_default_config, f_obj)
		
def play_reminder():
	try:
		config = load_config()
	except FileNotFoundError:
		pass
	else:
		if config['alert_noise'] == True:
			print(str(datetime.datetime.now().time()) + ": Reminder Played")
			winsound.PlaySound(
				'sounds//reminder.wav', winsound.SND_FILENAME)
		else:
			print(str(datetime.datetime.now().time()) + ": Reminder Muted")
	
def reset_last_reminder_time():
	global last_reminder_time
	last_reminder_time = time.time()
		
def time_interval_passed():
	current_time = time.time()
	time_difference = current_time - last_reminder_time
	if time_difference > settings.reminder_interval:
		return True
	else:
		return False
		
def time_until_intersect():
	current_time = time.time()
	seconds_until_intersect = graph_intersect_time - current_time
	minutes_until_intersect = round(((seconds_until_intersect / 60)), 1)
	if minutes_until_intersect > 0:
		return ("Time until behind schedule: {} minutes".format(
			minutes_until_intersect))
	else:
		return ("Currently behind schedule")
		
def update_graphs_intersect_time():
	data = load_data()
	y = int(data['y2'][-1])
	initial_time = data['alarm_time']
	intersect_time_hours = (
		(settings.day_hours * (y - settings.morning_intake)) /
		(settings.actual_daily_intake_ - settings.morning_intake)
		)
	intersect_time_seconds = intersect_time_hours * 60 * 60
	global graph_intersect_time
	graph_intersect_time = initial_time + intersect_time_seconds
	
# Initialization functions:
update_settings()
