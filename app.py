from datetime import datetime
from email.message import EmailMessage
from main import timetable, homework, name
import smtplib
from dotenv import load_dotenv
import os


# load_dotenv()

def format_date_readably(date_str):
    """
    Converts a date string in 'DD/MM/YYYY' format to 'Weekday the DayWithOrdinal'
    Example: '24/12/2024' → 'Tuesday the 24th'
    """
    try:
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        weekday = date_obj.strftime("%A")
        day = date_obj.day

        def ordinal(n):
            return f"{n}{'th' if 11 <= n <= 13 else {1:'st', 2:'nd', 3:'rd'}.get(n % 10, 'th')}"

        return f"{weekday} the {ordinal(day)}"
    except ValueError:
        return "Invalid date format. Please use 'DD/MM/YYYY'."

def holiday():

    exit()

def get_today_schedule():
    try:
        today = datetime.now().strftime("%A")
        schedule = timetable[today]
        if schedule:
            return schedule
        else:
            holiday()
    except KeyError:
        holiday()


schedule = get_today_schedule()
message = f"""
Hello {name.split()[0]}!

Today's timetable is:\n
"""
for period in schedule:
    message += f"{period['period']}) {period['subject']} in {period['room']}\n"
if len(homework) > 7:
    message += f"\nHere is your home learning for the week. Remember, you have Sparx too. You have a lot of home learning this week, {name.split()[0]}... Good Luck!"
elif len(homework) <= 7:
    message += f"\nHere is your home learning for the week. Remember, you have Sparx too. You only have {len(homework)} pieces of homework, {name.split()[0]}... It's easy this week!\n"

message += "The homework pending for this week is:\n"

for work in homework:
    message += f"• {work['title']} ({format_date_readably(work['due_Date'])}) - Set by {work['teacher']} for {work['subject']}\n"

message += "\n - The ClassNowX Team"



sender = os.environ["SENDER"]
receiver  = os.environ["RECEIVER"]
password = os.environ["SENDER_PASSWORD"]
subject = "Your daily Snapshot"
body = message

msg = EmailMessage()
msg["Subject"] = "Your daily Snapshot"
msg["From"] = sender
msg["To"] = receiver
msg.set_content(body)


server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(sender, password)
server.send_message(msg)
server.quit()

