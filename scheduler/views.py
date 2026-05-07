from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from .models import Meeting
import csv

@login_required
def dashboard(request):
    meetings = Meeting.objects.filter(user=request.user).order_by('-date_time')
    return render(request, 'dashboard.html', {'meetings': meetings})

@login_required
def manage_meeting(request, pk=None):
    # If pk exists, we are EDITING; otherwise, we are ADDING
    instance = get_object_or_404(Meeting, pk=pk, user=request.user) if pk else None

    if request.method == "POST":
        title = request.POST.get('title')
        date_time = request.POST.get('date_time')
        emails = request.POST.get('emails')
        send_to_gmail = request.POST.get('send_to_gmail') == 'on'

        if instance:
            instance.title, instance.date_time, instance.emails = title, date_time, emails
            instance.save()
            meeting = instance
        else:
            meeting = Meeting.objects.create(user=request.user, title=title, date_time=date_time, emails=emails)

        if send_to_gmail:
            recipient_list = [e.strip() for e in emails.split(',') if e.strip()]
            send_mail(
                f'Upcoming Meeting: {title}',
                f'You have a scheduled meeting on {date_time}. Please check your calendar.',
                'your-email@gmail.com', # Must match settings.py
                recipient_list,
                fail_silently=False,
            )
        return redirect('dashboard')

    return render(request, 'meeting_form.html', {'meeting': instance})

@login_required
def delete_meeting(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk, user=request.user)
    meeting.delete()
    return redirect('dashboard')

@login_required
def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="my_meetings.csv"'
    writer = csv.writer(response)
    writer.writerow(['Title', 'Date & Time', 'Recipients'])
    for m in Meeting.objects.filter(user=request.user):
        writer.writerow([m.title, m.date_time, m.emails])
    return response
