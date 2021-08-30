import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Q

from .models import Topic, Entry
from .forms import TopicForm, EntryForm, CommentForm

# Create your views here.
def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')

def topics(request):
    """Show all topics."""
    # Restricted access.
    if request.user.is_authenticated:
        topics = Topic.objects.filter(Q(owner=request.user) | Q (public=True)).order_by('date_added')
    else:
        topics = Topic.objects.filter(public=True).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    """Show a single topic, all of its entries and comments."""
    topic = get_object_or_404(Topic, id=topic_id)
    # Make sure the topic belongs to the current user.
    check_topic_availability(request, topic)
    
    entries = topic.entry_set.order_by('-date_added')
    comments = topic.comment_set.order_by('-date_added')
    new_comment = None
    
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = CommentForm()
    else:
        # POST data submitted; process data.
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.topic = topic
            new_comment.author = request.user
            new_comment.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    # Display a blank or invalid form.
    context = {'topic': topic,
               'entries': entries,
               'comments': comments,
               'new_comment': new_comment,
               'form': form}

    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def edit_topic(request, topic_id):
    """Edit an existing topic."""
    topic = get_object_or_404(Topic, id=topic_id)
    # Make sure the topic belongs to the current user.
    check_topic_ownership(request, topic)

    if request.method != 'POST':
        # Initial request; pre-fill with the current entry.
        form = TopicForm(instance=topic)
    else:
        # POST data submitted; process data.
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = get_object_or_404(Topic, id=topic_id)
    # Make sure the topic belongs to the current user.
    check_topic_ownership(request, topic)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    #Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    # Make sure the topic belongs to the current user.
    check_topic_ownership(request, topic)

    if request.method != 'POST':
        # Initial request; pre-fill with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

def check_topic_availability(request, topic):
    """
        Make sure the user currently logged in
        has the right to view the topic.
    """
    if topic.owner != request.user and not topic.public:
        raise Http404

def check_topic_ownership(request, topic):
    """
        Make sure the user currently logged in
        matches the owner of the topic.
    """
    if topic.owner != request.user:
        raise Http404