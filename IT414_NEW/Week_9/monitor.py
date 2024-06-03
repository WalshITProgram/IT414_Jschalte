import psutil
import smtplib
from twilio.rest import Client
import json
from datetime import datetime, timedelta
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

# Setup logging
logging.basicConfig(filename='monitor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
with open('text_files/script_config.json') as config_file:
    config = json.load(config_file)

MAIL_SERVER = config['mail_server']
MAIL_PORT = config['mail_port']
USERNAME = config['username']
PASSWORD = config['password']
FROM_EMAIL = config['from_email']
TO_EMAIL = config['to_email']
TWILIO_ACCOUNT_ID = config['twilio_account_id']
TWILIO_AUTH_TOKEN = config['twilio_auth_token']
TWILIO_TRIAL_NUMBER = config['twilio_trial_number']
TWILIO_CELL_NUMBER = config['twilio_cell_number']
LAST_TEXT = config['last_text']

def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = TO_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
        server.starttls()
        server.login(USERNAME, PASSWORD)
        text = msg.as_string()
        server.sendmail(FROM_EMAIL, TO_EMAIL, text)
        server.quit()
        logging.info("Email sent successfully")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

def send_text(alert_text):
    try:
        client = Client(TWILIO_ACCOUNT_ID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=alert_text,
            from_=TWILIO_TRIAL_NUMBER,
            to=TWILIO_CELL_NUMBER
        )
        logging.info("Text message sent successfully")
    except Exception as e:
        logging.error(f"Failed to send text message: {e}")

def check_thresholds(cpu_usage, memory_usage, disk_usage, net_io):
    alerts = []
    if cpu_usage > 85:
        alerts.append(f"CPU usage is at {cpu_usage}% which exceeds the threshold.")
    if memory_usage > 90:
        alerts.append(f"Memory usage is at {memory_usage}% which exceeds the threshold.")
    for disk in disk_usage:
        if disk['percent'] > 70:
            alerts.append(f"Disk {disk['device']} usage is at {disk['percent']}% which exceeds the threshold.")
    if net_io['errors'] > 0 or net_io['dropped'] > 0:
        alerts.append(f"Network errors or dropped packets detected. Errors: {net_io['errors']}, Dropped: {net_io['dropped']}.")

    return alerts

def get_system_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    disk_usage = [{'device': part.device, 'percent': psutil.disk_usage(part.mountpoint).percent} for part in psutil.disk_partitions()]
    net_io = psutil.net_io_counters()
    net_errors = psutil.net_if_stats()
    errors = sum([stat.errin + stat.errout for stat in net_errors.values()])
    dropped = sum([stat.dropin + stat.dropout for stat in net_errors.values()])
    return {
        'cpu': cpu_usage,
        'memory': memory_usage,
        'disk': disk_usage,
        'network': {'bytes_sent': net_io.bytes_sent, 'bytes_recv': net_io.bytes_recv, 'errors': errors, 'dropped': dropped}
    }

def generate_report():
    metrics = get_system_metrics()
    now = datetime.now().strftime("%B %d, %Y %H:%M:%S")
    report = f"""
    Time of Report: {now}
    CPU Usage: {metrics['cpu']}%
    Memory Usage: {metrics['memory']}%
    Disk Usage: {', '.join([f"{disk['device']}: {disk['percent']}%" for disk in metrics['disk']])}
    Network: Bytes Sent: {metrics['network']['bytes_sent']}, Bytes Received: {metrics['network']['bytes_recv']}, Errors: {metrics['network']['errors']}, Dropped: {metrics['network']['dropped']}
    """
    return report

def send_alerts():
    metrics = get_system_metrics()
    alerts = check_thresholds(metrics['cpu'], metrics['memory'], metrics['disk'], metrics['network'])
    if alerts:
        now = datetime.now().strftime("%B %d, %Y %H:%M:%S")
        alert_text = f"{now} - {'; '.join(alerts)}"
        last_text_time = datetime.strptime(config['last_text'], "%Y-%m-%d %H:%M:%S") if config['last_text'] else datetime.now() - timedelta(hours=2)
        if datetime.now() - last_text_time > timedelta(hours=1):
            send_text(alert_text)
            config['last_text'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('text_files/script_config.json', 'w') as config_file:
                json.dump(config, config_file)

def job():
    send_alerts()
    report = generate_report()
    send_email('System Resource Report', report)

schedule.every().day.at("06:00").do(job)
schedule.every().day.at("18:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
