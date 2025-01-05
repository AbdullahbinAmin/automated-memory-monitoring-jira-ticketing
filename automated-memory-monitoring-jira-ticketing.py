import time
import smtplib
import paramiko
from jira import JIRA
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Server and SSH credentials
hostname = "YOUR SERVER IP ADDRESS"
username = "YOUR USERNAME"
password = "YOUR PASSWORD"

# JIRA User credentials and API Key
user = "YOUR JIRA ACCOUNT EMAIL"
api_key = 'YOUR JIRA ACCOUNT API KEY'

# JIRA Server URL
server = "YOUR JIRA ATLASSIAN WEBSITE LINK"

# Connect to JIRA
jira = JIRA(server=server, basic_auth=(user, api_key))

# SSH Client Setup
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=hostname, username=username, password=password)

# Command to check available memory
cmd = "free -g"
std_in, std_out, std_error = client.exec_command(cmd)

# Output of the command
cmdout = std_out.readlines()
for i in cmdout:
    print(i)

# Extract available memory from the command output
available_memory = cmdout[1].split()[6]

# Check if the available memory is less than or equal to 1GB
if int(available_memory) <= 1:
    print(f"Alert: Available memory on server {hostname} is critically low ({available_memory}GB).")

    # Prepare the issue details
    Summary = f"Memory Available: {available_memory}GB"
    Description = f"""Dear Team,

    A memory shortage has been detected on the server {hostname}.
    Available memory: {available_memory}GB.

    This is a critical issue that requires your immediate attention.
    Please review and take appropriate action to resolve the memory shortage.

    Thank you,
    Al-Nafi Support Team
    """

    # Issue details for creating the JIRA ticket
    issue_dict = {
        'project': {'key': 'IIP'},
        'issuetype': {'name': 'Issue'},
        'description': Description,
        'summary': Summary,
        'priority': {'name': 'Highest'},
        'timetracking': {'originalEstimate': '1h'},
        'assignee': {"accountId": "YOUR JIRA ACCOUNT ID"} # Specify stakeholder account ID
    }

    # Create the JIRA issue
    new_issue = jira.create_issue(fields=issue_dict)
    print(f'Ticket created and assigned to the stakeholder. Issue ID: {new_issue.key}')

    # Send Email to Reporter for Manager Approval
    email_subject = f"Approval Request for Ticket {new_issue.key}: {Summary}"
    email_body = f"""
        <p>Dear Reporter,</p>
        <p>Thank you for writing to us.</p>
        <p>We have received your JIRA ticket <strong>{new_issue.key}: {Summary}</strong> for a server access request.</p>
        <p>Please provide the approval from your reporting head for proceeding further. Our team is looking into the issue and we will get back to you as quickly as possible.</p>
        <p>In case of immediate assistance, please dial the Al-Nafi Direct lines for a quick response.</p>
        <p>We look forward to interacting soon!</p>
        <p>Best regards,<br>Al-Nafi Support Team</p>
        """

    # Fetch the reporter's email
    reporter_email = new_issue.fields.reporter.emailAddress

    # Send the approval request email
    my_mail = "YOUR EMAIL"
    password = "YOUR EMAIL APP PASSWORD"

    msg = MIMEMultipart()
    msg['Subject'] = email_subject
    msg['From'] = my_mail
    msg['To'] = reporter_email
    msg.attach(MIMEText(email_body, 'html'))

    # SMTP server setup
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()  # Secure connection
        connection.login(user=my_mail, password=password)
        connection.send_message(msg)
        print(f"Approval email sent to {reporter_email}")

else:
    print(f"Memory status on {hostname} is optimal. Available memory: {available_memory}GB.")