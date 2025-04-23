from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models import Q

from .models import Event, Contact, Invitation, Post, RSVP, Notification, Friend
from .forms import EventForm, ContactForm, PostForm

@login_required
def index(request):
    events = Event.objects.all()
    return render(request, 'events/index.html', {'events': events})

@login_required
def home(request):
    events = Event.objects.all()
    return render(request, 'events/home.html', {'events': events})

@login_required
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, "Event created successfully!")
            return redirect('home')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    posts = Post.objects.filter(event=event).order_by('-created_at')
    notifications = Notification.objects.filter(user=request.user, post__event=event, read=False)
    return render(request, 'events/event_detail.html', {
        'event': event,
        'posts': posts,
        'notifications': notifications
    })

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.created_by != request.user:
        messages.error(request, "You do not have permission to edit this event.")
        return redirect('event_detail', event_id=event.id)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('home')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/edit_event.html', {'form': form, 'event': event})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.created_by != request.user:
        messages.error(request, "You do not have permission to delete this event.")
        return redirect('event_detail', event_id=event.id)

    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect('home')

    return render(request, 'events/delete_event.html', {'event': event})

@login_required
def send_invitations(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    contacts = Contact.objects.filter(user=request.user)

    if request.method == 'POST':
        contact_ids = request.POST.getlist('contacts')
        for contact_id in contact_ids:
            contact = Contact.objects.get(id=contact_id)
            invitation, created = Invitation.objects.get_or_create(event=event, invitee=contact.email)
            if created:
                invitation.phone = contact.phone
                invitation.save()
                send_mail(
                    subject=f"Invitation to {event.name}",
                    message=f"You are invited to {event.name} at {event.location} on {event.date} {event.time}.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[contact.email],
                    fail_silently=True,
                )
        messages.success(request, "Invitations sent successfully!")
        return redirect('event_detail', event_id=event.id)

    return render(request, 'events/send_invitations.html', {'event': event, 'contacts': contacts})

@login_required
def rsvp_event(request, event_id, response):
    event = get_object_or_404(Event, id=event_id)
    RSVP.objects.update_or_create(
        event=event,
        user=request.user,
        defaults={'response': response},
    )
    messages.success(request, f'RSVP: {response}')
    return redirect('event_detail', event_id=event.id)

@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            messages.success(request, "Contact added successfully!")
            return redirect('add_contact')
    else:
        form = ContactForm()
    return render(request, 'events/add_contact.html', {'form': form})

@login_required
def create_post(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.event = event
            post.created_by = request.user
            post.save()
            notify_users_about_post(post)
            messages.success(request, "Post created and notifications sent!")
            return redirect('event_detail', event_id=event.id)
    else:
        form = PostForm()
    return render(request, 'events/create_post.html', {'form': form, 'event': event})

def notify_users_about_post(post):
    event = post.event
    invited_emails = Invitation.objects.filter(event=event).values_list('invitee', flat=True)
    invited_users = User.objects.filter(email__in=invited_emails)
    friends = Friend.objects.filter(user=post.created_by).values_list('friend', flat=True)
    mutual_users = User.objects.filter(id__in=friends)
    users_to_notify = set(invited_users) | set(mutual_users)

    for user in users_to_notify:
        Notification.objects.create(post=post, user=user)

@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(user=request.user, read=False).order_by('-notified_at')
    return render(request, 'events/notifications.html', {'notifications': notifications})

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.read = True
    notification.save()
    return redirect('notifications_list')

def profile_view(request):
    return render(request, 'events/profile.html')
