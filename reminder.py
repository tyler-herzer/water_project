import time
import water_functions as wf

# Initializations:
wf.initialize_config()

# Main loop:
while True:
	wf.check_reminder() # Play reminder if appropriate.
	time.sleep(300) # 120 second break to reduce CPU usage.
