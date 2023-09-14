import schedule
import time
import subprocess

def run_task():
    subprocess.run(["python", "data_drift_code.py"])

# Execute the task immediately
run_task()

# Schedule the task to run every 10 days
# schedule.every(10).days.do(run_task)