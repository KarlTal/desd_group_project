from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from AccountManager.forms import *
from UWEFlix.decorators import allowed_users


# The handler for the homepage of the website.
@login_required(login_url='/login')
@allowed_users(allowed_roles='AccountManager')
def home(request):
    users = User.objects.all()
    profiles = UserProfile.objects.all()
    return render(request, 'AccountManager/home.html', {'users': users, 'profiles': profiles})


# Handle editing users.
@login_required(login_url='/login')
@allowed_users(allowed_roles='AccountManager')
def update_user(request, user_id):
    # If the showing_id exists and the form is valid, update the Showing database object with the data from the form.
    if user_id:
        user_lookup = User.objects.get(id=user_id)
        profile_lookup = UserProfile.objects.get(user_obj=user_lookup)

        if user_lookup and profile_lookup:
            user_form = UserForm(request.POST or None, instance=user_lookup)
            profile_form = UserProfileForm(request.POST or None, instance=profile_lookup)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect(home)

            # Render the page.
            return render(request, 'AccountManager/update_user.html', {'user': user_lookup, 'profile': profile_lookup,
                                                                       'user_form': user_form,
                                                                       'profile_form': profile_form})

    # Redirect back to the homepage.
    return redirect(cinema_dashboard)


# The handler for deleting a screen.
@login_required(login_url='/login')
@allowed_users(allowed_roles='AccountManager')
def delete_user(request, user_id):
    # If a user_id is provided, lookup the User object and delete it.
    if user_id:
        lookup = User.objects.get(user=user_id)
        lookup.delete()

    # Redirect back to the homepage.
    return redirect(home)
