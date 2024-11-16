from django.utils import timezone
from datetime import timedelta
from .models import Message
from .forms import MessageForm
import pywhatkit as kit
from django.shortcuts import redirect, render
import threading

def schedule_message(message):
    now = timezone.now()
    send_time = message.send_time

    # Calculate delay in seconds
    delay = (send_time - now).total_seconds()

    if delay > 0:
        # Schedule the message to be sent
        def send_message():
            try:
                # Open WhatsApp Web and send the message
                kit.sendwhatmsg_instantly(
                    phone_no=message.phone,
                    message=message.message,
                    wait_time=10,  # Adjust the wait time as needed
                    tab_close=True,  # Close the browser tab after sending
                )
                message.status = 'sent'
            except Exception as e:
                message.status = 'failed'
            finally:
                message.save()

        # Start the sending task at the scheduled time
        threading.Timer(delay, send_message).start()

def home(request):
    messages = Message.objects.all()
    form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            send_time = form.cleaned_data['send_time']

            # Check if there is a pending message with the same phone number
            # but allow scheduling with a different time
            existing_message = Message.objects.filter(phone=phone, status='pending').first()
            if existing_message and existing_message.send_time == send_time:
                return render(request, 'home.html', {
                    'form': form,
                    'messages': messages,
                    'error': 'A message is already scheduled for this number at the same time.'
                })

            # Save the new message
            new_message = form.save(commit=False)
            new_message.status = 'pending'
            new_message.save()

            # Schedule the message
            schedule_message(new_message)

            return redirect('home')

    return render(request, 'home.html', {'form': form, 'messages': messages})
