# 📅 Event Scheduler Web Application

A full-featured Django web application that allows users to manage personal events with categorization, conflict prevention, and automatic email reminders using Celery.

## ✨ Features

- 🔐 **User Authentication** – Register, login, logout (custom registration with email)
- 📝 **Event Management** – Create, Read, Update, Delete events
- 🏷️ **Event Categories** – Work, Personal, Meeting, etc. (customizable via admin)
- ⚠️ **Conflict Prevention** – No two events for the same user on same date/time
- 📧 **Email Reminders** – Automatic reminders for upcoming events (using Celery)
- 👑 **Admin Panel** – Super admin can view/manage all events, users, categories
- 🎨 **Responsive UI** – Bootstrap 5 with modern gradient design

## 🛠️ Tech Stack

- **Backend:** Django 5.x, Python 3.10+
- **Task Queue:** Celery with Redis broker
- **Database:** SQLite (default), can switch to PostgreSQL/MySQL
- **Frontend:** Bootstrap 5, HTML5, Django Template Language
- **Email:** Console backend for development (SMTP ready for production)

## 📋 Prerequisites

- Python 3.10 or higher
- Redis server (for Celery)
- Git (optional)

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/event-scheduler.git
cd event-scheduler


🚀 Optional Enhancements
Add start_datetime field to Event for more precise reminder queries (instead of combining date+time each time).

Use real email backend (SMTP) for production.

Allow users to set reminder offset (e.g., 1 hour before, 1 day before) per event.

Add in-app notifications alongside email.

Now your Event Scheduler is fully functional with admin oversight, categories, and automated email reminders via Celery!

# How To Run:
2. Create virtual environment
bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
3. Install dependencies
bash
pip install -r requirements.txt
If requirements.txt is not available, install manually:

bash
pip install django celery redis django-celery-beat
4. Configure environment variables (optional)
Create a .env file or set directly in settings.py. For development, defaults work.

5. Run migrations
bash
python manage.py makemigrations events
python manage.py migrate
6. Create superuser (admin)
bash
python manage.py createsuperuser
7. Create default categories (optional)
Via admin or run:

bash
python manage.py shell
>>> from events.models import Category
>>> categories = ['Work', 'Personal', 'Meeting', 'Reminder', 'Health']
>>> for cat in categories: Category.objects.get_or_create(name=cat, slug=cat.lower())
8. Start Redis server
macOS (Homebrew):

bash
brew install redis
redis-server
Linux (Ubuntu/Debian):

bash
sudo apt install redis-server
redis-server
Windows: Download from https://github.com/microsoftarchive/redis/releases

9. Start Celery worker (new terminal)
bash
celery -A event_scheduler worker -l info
10. Start Celery beat scheduler (another terminal)
bash
celery -A event_scheduler beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
11. Run Django development server
bash
python manage.py runserver
Visit http://127.0.0.1:8000

🧪 Testing
Run the test suite:

bash
python manage.py test events
Expected output: OK (all tests pass).

🖥️ Usage Guide
For Regular Users
Register – Provide username, email, password.

Login – Use your credentials.

Create Event – Fill name, date, time, description, optional category.

View Events – See all your events in card grid.

Edit/Delete – Modify or remove events.

Receive Reminders – If you provided an email, you'll get reminders for events starting within 1 hour.

For Admin (Superuser)
Access /admin panel.

Manage all users, events, categories.

Monitor Celery periodic tasks under django_celery_beat.

Add/remove categories.

📧 Email Configuration
Development (console)
Already set in settings.py:

python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
Emails will be printed in the terminal where the Celery worker runs.


⏰ How Reminders Work
Celery Beat runs a periodic task every hour (check_upcoming_events).

It finds events with reminder_sent=False and start time within next hour.

For each such event, it queues a send_event_reminder task.

The Celery worker sends an email to the user's registered email.

The event is marked reminder_sent=True to avoid duplicates.

Production (SMTP example with Gmail)
python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'

🐛 Troubleshooting
Problem	Solution
Registration fails	Check terminal for form errors; ensure password is strong (e.g., StrongPass123!)
Category dropdown empty	Create categories via admin (/admin/events/category/)
Reminders not sent	Verify Redis is running, Celery worker and beat are active, and users have email addresses
NoReverseMatch: 'event-list'	Ensure LOGIN_REDIRECT_URL = 'event-list' in settings.py
Celery can't connect to Redis	Start Redis: redis-server

🔧 Customization
Change reminder offset – Modify timedelta(hours=1) in tasks.py

Add more fields – Extend Event model and update forms/templates

Use PostgreSQL – Install psycopg2 and update DATABASES in settings.py

🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first.





🙏 Acknowledgements
Django documentation

Celery documentation

Bootstrap 5