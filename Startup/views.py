import datetime
from sqlite3 import IntegrityError
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import (
    Attendance,
    classes as Classes,
    memberships as Membership,
    payment as Payment,
    TrainerProfile,
    trainer,
    UserProfile
)
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
def index (request):
  
     return render(request,'index.html')
def Home(request):
     return render(request,'Home.html')
def logout(request):
    return render(request,'index.html')
def about(request):
     return render(request,'about.html')
def trainners(request):
    dict_tr={
        'train':trainer.objects.all()
    }
    return render(request,'trainers.html',dict_tr)
def memberships(request):
      return render(request,'membership.html')
def contact(request):
      return render(request,'contact.html')
def loginn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pswrd = request.POST.get('password')
        user = authenticate(username=username,password=pswrd)
        if user is not None:
            login(request,user)
            
            return redirect('Home') 
        else:
            messages.error(request, "Invalid username or password.")
       
            return redirect('signup')
      
    return render(request,'login.html') 

def signupp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        '''gen= request.POST.get('gender')
        age = request.POST.get('age')'''
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        is_trainer = request.POST.get('is_trainer') == 'on'

        if password != password_confirm:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if username and email and password:
            try:
                try:
                    validate_password(password)
                except ValidationError as e:
                    messages.error(request, e.messages[0])  # Show first validation error message
                    return redirect('signup')

                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already exists")
                    return redirect('signup')

                if User.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists")
                    return redirect('signup')

                
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                UserProfile.objects.create(user=user, is_trainer=is_trainer)
                messages.success(request, "User registered successfully")
                return redirect('login')
            
            except IntegrityError:
                messages.error(request, "An error occurred during registration")
                return redirect('signup')

        else:
            messages.error(request, "Please fill all fields")
            return redirect('signup')


    return render(request, 'signup.html')
def profile(request):
    user = request.user
    try:
        memberships = Membership.objects.get(user=user)  # Get the user's memberships
    except Membership.DoesNotExist:
        memberships = None  # In case the user has no memberships

    return render(request, 'profile.html', {'memberships': memberships})
def payment_view(request, method):
    if request.method == 'POST':
        username = request.POST.get('username')
        plan = request.POST.get('plan')
        amount = request.POST.get('amount')
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')

        
        
#validate the amount
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
        except ValueError:
            messages.error(request, "Invalid amount entered.")
            return redirect('payment', method=method)

        # Retrieve the user by username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('payment', method=method)

        # Create payment record
        payment = Payment(
            user=user,
            amount=amount,
            plan=plan,
            card_number=card_number,  # Consider encrypting this
            expiry_date=expiry_date,  # Consider validation for expiry date
            cvv=cvv,                  # Consider encrypting this
            method=method,
            status="Success"  # Set status as success
        )

        # Save the payment to the database
        payment.save()
        request.session['user_plan'] = plan

       
        memberships, created = Membership.objects.get_or_create(user=user)

        
        
        memberships.remaining_classes = 30 

        messages.success(request, "Payment successful, and memberships updated.")
        return redirect('payment_success')  

        

    return render(request, 'payment.html', {'method': method})
def payment_success_view(request):

    # Retrieve the plan from the session
     user_plan = request.session.get('user_plan')
    
    # Check if the user chose the premium plan
     context = {'is_premium': user_plan == 'premium'}
    
     return render(request, 'payment_success.html', context)
@login_required(login_url='/login/')
    # Check if the logged-in user is an approved trainer
def attendance_mark(request):
    # Check if the logged-in user is an approved trainer
    profile = TrainerProfile.objects.filter(user=request.user).first()  # Using filter with first() to avoid exception
    if profile:
        if not profile.is_approved:
            messages.error(request, "You are not approved as a trainer and cannot mark attendance.")
            return redirect('home')  # Redirect unapproved trainers to another page
    else:
        messages.error(request, "Trainer profile not found.")
        return redirect('login')

    if request.method == 'POST':
        selected_usernames = request.POST.getlist('usernames')  # Get selected usernames
        date = request.POST.get('date')  # Get the selected date

        if selected_usernames:
            attendance_marked = False  # Track if attendance was marked for any user

            for username in selected_usernames:
                try:
                    # Get the user object by username
                    user_to_mark = User.objects.get(username=username)

                    # Check if attendance is already marked for this user on the specified date
                    if Attendance.objects.filter(user=user_to_mark, date=date).exists():
                        messages.warning(request, f"Attendance for {user_to_mark.username} on {date} is already marked.")
                        continue  # Skip to the next user

                    # Store attendance in the database
                    Attendance.objects.create(user=user_to_mark, date=date)
                    attendance_marked = True  # Set flag to indicate attendance was marked

                    # Fetch the user's memberships
                    memberships = Membership.objects.get(user=user_to_mark)

                    # Reduce remaining classes if they have any left
                    if memberships.remaining_classes > 0:
                        memberships.remaining_classes -= 1
                        memberships.save()  # Save the updated memberships
                    else:
                        # Handle unexpected cases where remaining_classes is negative
                        memberships.remaining_classes = 0
                        memberships.save()  # Set remaining_classes to 0 to avoid negatives
                        messages.error(request, f"{user_to_mark.username} has no remaining classes.")
                
                except User.DoesNotExist:
                    messages.error(request, f"User {username} does not exist.")
                except Membership.DoesNotExist:
                    messages.error(request, f"No memberships found for {username}.")

            # Show success message only if attendance was marked for any user
            if attendance_marked:
                messages.success(request, "Attendance marked successfully for valid users.")
        else:
            messages.error(request, "Please select at least one user.")

    # Fetch payments that have users and filter by successful payments
    payments = Payment.objects.filter(status="Success").select_related('user')

    return render(request, 'attendance_mark.html', {'payments': payments})

def unapproved_trainer(request):
    return render(request, 'unapproved_trainer.html')
def classes(request):
    return render(request,'classes.html')
def trainer_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.is_approved:  # Check if the user is an approved trainer
                    login(request, user)
                    return redirect('attendance_mark')  # Redirect to attendance marking page
                else:
                 messages.error(request, "Your trainer profile is not yet approved. Please contact the admin.")
            except TrainerProfile.DoesNotExist:
                return HttpResponse("Trainer profile not found. Please contact admin.")
        else:
            return HttpResponse("Invalid credentials.")

    return render(request, 'trainer_login.html')
def update(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        profile =TrainerProfile.objects.get(user=request.user)  # Assuming a user field is linked
        profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        return redirect('profile')
    return render(request, 'updateprofile.html')
def expired_memberships_view(request):
    # Get users whose remaining classes = 0
    expired_memberships = Membership.objects.filter(remaining_classes__lte=0)
    
    # Pass the expired memberships to the template
    return render(request, 'expired.html', {'expired_memberships': expired_memberships})
def book_class_view(request):
    user_memberships = Membership.objects.get(user=request.user)
    
    # Check if user has a personal training plan with remaining classes
      # Redirect to an appropriate page

    if request.method == "POST":
        # Retrieve data from the form
        date = request.POST.get('date')
        time = request.POST.get('time')
        trainer_id = request.POST.get('trainer')
        
        # Check if all fields are filled
        if date and time and trainer_id:
            trainer = TrainerProfile.objects.get(id=trainer_id)
            existing_booking = ClassBooking.objects.filter(trainer=trainer, date=date, time=time).first()
            if existing_booking:
                # If the trainer is already booked, show an error message
                messages.error(request, f"{trainer.user.username} is already booked for this time.")
                return redirect('book_class')
            # Save booking
            booking = ClassBooking(
                user=request.user,
                trainer=trainer,
                date=date,
                time=time,
                status='Booked'
            )
            booking.save()
            
            # Deduct remaining classes
            user_memberships.remaining_classes -= 1
            user_memberships.save()
            
            messages.success(request, "Your class has been successfully booked!")
            return redirect('bookedclass')  # Redirect to a page showing bookings
        else:
            messages.error(request, "Please fill in all the fields.")
            return redirect('book_class')
    
    # Get list of trainers to populate the dropdown
    
    trainers = TrainerProfile.objects.filter(is_approved=True)
    return render(request, 'booking.html', {'trainers': trainers})
def select_date_time(request):
    if request.method == 'POST':
        selected_date = request.POST.get('date')
        selected_time = request.POST.get('time')
        selected_trainer = request.POST.get('trainer')
        
        # Store in session or pass as query params
        request.session['selected_date'] = selected_date
        request.session['selected_time'] = selected_time
        request.session['selected_trainer'] = selected_trainer
          # Redirect to the trainers view
        trainers = TrainerProfile.objects.filter(is_approved=True)
    return render(request, 'select_date_time.html')
def bookedclass(request):
    return render(request,'schedules.html')
def trainer_class_bookings(request):
    try:
        trainer_profile = TrainerProfile.objects.get(user=request.user)
    except TrainerProfile.DoesNotExist:
        # If the trainer is not found, return an error or redirect to another page
        messages.error(request, "Trainer profile not found.")
        return redirect('home')  # Adjust the redirection as needed

    # Get the bookings for this trainer (filter by the trainer's profile)
    bookings = ClassBooking.objects.filter(trainer=trainer_profile)

    # Pass the bookings to the template
    return render(request, 'viewbooking.html', {'bookings': bookings})