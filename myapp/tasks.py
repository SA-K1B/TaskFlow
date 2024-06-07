from celery import shared_task
from django.core.mail import send_mail
@shared_task
def send_email_task(subject, message, from_email, recipient_list,html_message= None):
#    try: 
     send_mail(subject, message, from_email, recipient_list,fail_silently = False,html_message=html_message)
#    except Exception as e:
#      print("Something is wrong")
