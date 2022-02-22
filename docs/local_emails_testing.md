# Sending E-mails via command

1. In `a4-meinberlin` activate `virtual env (venv)`.
2. Run `python manage.py send_test_emails [your email]`.
3. Check mailbox of the specified email.

File: meinberlin/apps/notifications/management/commands/send_test_emails.py

# Sending E-mails via background tasks

1. In `a4-meinberlin` activate `virtual env (venv)`.
2. Run `make background`.
3. Go to project in your browser.
4. Take actions (comment, report etc.) to trigger emails.
5. Check mailbox of email that gets notified.

File: Makefile
