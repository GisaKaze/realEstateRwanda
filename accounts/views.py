from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from contacts.models import Contact

def register(request):
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        # Check if passwords are the same
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already registered with other user')
                    return redirect('register')
                # Good to go
                else:
                    user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                    # Login after register
                    # auth.login(request, user)
                    # messages.success(request, "You're now logged in")
                    # return redirect('index')
                    user.save();
                    messages.success(request, "You're now registered and you can log in")
                    return redirect('login')
        else:
            # Error message
            messages.error(request, 'Password do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Wrong password or email')
            return redirect('login')
    
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, "You're logged-out")
        return redirect('index')


def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)
