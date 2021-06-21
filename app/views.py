import time

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView
from app.models import Massage
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import threading
from django.db.models import Q

# Create your views here.

threads=[]

class MassageList(ListView):
    model = Massage
    template_name = "massage_list.html"

    def get_queryset(self):
        n = Massage.objects.all().count()
        context = Massage.objects.all()
        if n >= 10:
            context = Massage.objects.all()[n - 10:n]
        return context


def sendMassage(from_e, to_e, text_e, delay):
    time.sleep(int(delay))
    message = Mail(
        from_email=from_e,
        to_emails=to_e,
        subject='Sending with Twilio SendGrid is Fun',
        html_content=str(text_e))
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.massage)
    temp = Massage.objects.filter(Q(text=text_e) & Q(text=text_e))
    temp.update(status=1)


def createMessage(request):
    if request.method == "POST":
        from_e = 'Dready@yandex.ru'
        to_e = request.POST.get("to_email")
        text_e = request.POST.get("text")
        delay = request.POST.get("delay")
        tom = Massage()
        tom.text = text_e
        tom.from_email = from_e
        tom.to_email = to_e
        tom.status = 0
        tom.save()
        t = threading.Thread(target=sendMassage, args=(from_e, to_e, text_e, delay,))
        threads.append(t)
        t.start()
        return HttpResponseRedirect("massages/")
    else:
        return render(request, 'send.html')

