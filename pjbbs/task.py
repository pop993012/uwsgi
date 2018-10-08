from c_app import *

from dysms_python.demo_sms_send import  send_sms

@celery_server.task
def SendSMS(a1,a2):
    r=send_sms(phone_numbers=a1,smscode=a2)
    return r