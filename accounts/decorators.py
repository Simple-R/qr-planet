# account/decorators.py

from django.shortcuts import redirect


# if user is already logged in, let him just be redirected to dashboard
def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper_function
