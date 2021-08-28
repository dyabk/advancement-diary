from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404

# Create your views here.
def register(request):
    """Register a new user."""
    check_authentication(request)

    if request.method != 'POST':
        # Display blank registration form.
        form = UserCreationForm()
    else:
        # Process completed form.
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Log the user and then redirect to home page.
            login(request, new_user)
            return redirect('learning_logs:index')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'registration/register.html', context)

def check_authentication(request):
    """
        Make sure the user won't create another user account
        while logged in.
    """
    if request.user.is_authenticated:
        raise Http404
