# scheduler.py
import schedule
import time
import subprocess

def run_monthly_task():
    subprocess.run(["python", "ci_cd_pipelies.py"])

# Execute the task immediately
run_monthly_task()

# Schedule the task to every month starting
# schedule.every().month.at("00:00").do(run_monthly_task)