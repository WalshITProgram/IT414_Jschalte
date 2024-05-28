# Setup Instructions

Setting up Scheduled Tasks

On Linux (using cron), Add the following lines to your crontab (crontab -e):

#cron
#0 0,6,12,18 * * * /usr/bin/python /path/to/Week_8/app.py

On Windows (using Task Scheduler)

#Open Task Scheduler.
#Create a new Basic Task.
#Set the task to run daily.
#Set the time to 00:00, 06:00, 12:00, and 18:00.
#Set the action to start a program and point to your Python executable and the script path.

## Running the Script

To run the script, use the following command:

```bash
python app.py