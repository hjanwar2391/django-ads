from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout as auth_logout, get_user_model
from .forms import CustomUserCreationForm, LoginForm, ReferenceForm, VideoForm
from .models import User, UserAdView, Reference, Ad
from django.utils.timezone import now, timedelta
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from .models import Withdrawal
from .forms import WithdrawalForm
from .models import Notification

# Dynamically get the custom user model



# this is home page area
def homepage(request):
    return render(request, "home.html")



# registation area here
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login_view")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})



User = get_user_model()  # Fetch the custom user model



# login area herea
def login_view(request):
    error_message = None  # To store any error message
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            # Authenticate user
            user = authenticate(request, email=email, password=password)

            if user is not None:
                # Check user status and redirect accordingly
                if user.status == "pending":
                    login(request, user)
                    return render(request, "status_pending.html")  # Redirect to a pending status page
                elif user.status == "checking":
                    login(request, user)
                    return render(request, "status_checking.html")  # Redirect to a checking status page
                elif user.status == "active" or user.is_superuser:  # Allow both active users and superusers
                    login(request, user)  # Log in the user
                    return redirect("homepage")  # Redirect to the homepage or dashboard
            else:
                # If authentication fails, set error message
                if not User.objects.filter(email=email).exists():
                    error_message = "Account with this email does not exist."
                else:
                    error_message = "Invalid email or password."
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form, "error_message": error_message})




# logout area here
def logout(request):
    auth_logout(request)
    return redirect("login_view")




# status_pending area for user
@login_required
def status_pending(request):
    return render(request, "status_pending.html")




# status chenging area for user
@login_required
def status_checking(request):
    return render(request, "status_checking.html")




# notification area for user
@login_required
def notification(request):
    notifications = Notification.objects.all()
    return render(request, 'notification.html', {"notifications": notifications})



#  dashboard area for user
@login_required
def dashboard(request):
    wallet = request.user.wallet
    notifications = Notification.objects.all()

    # Pass both wallet and notifications in a single dictionary
    context = {
        "wallet": wallet,
        "notifications": notifications,
        "wallet_points": wallet.points,
    }

    return render(request, "dashboard.html", context)




# ads view area for user
@login_required
def view_ads(request):
    # Check if any ads are available
    ads_count = Ad.objects.count()
    if ads_count == 0:
        return render(
            request, "no_ads_available.html"
        )  # Show a page saying no ads are available

    # Count how many ads the user has already viewed today
    today_views_count = UserAdView.objects.filter(
        user=request.user, viewed_at__date=now().date()
    ).count()

    # Limit to 3 views per day
    if today_views_count >= 3:
        return render(request, "limit_reached.html")

    # Get the next ad that the user hasn't viewed today
    ads_viewed_today = UserAdView.objects.filter(
        user=request.user, viewed_at__date=now().date()
    ).values_list("ad_id", flat=True)
    next_ad = Ad.objects.exclude(id__in=ads_viewed_today).first()
    

    if next_ad:
        # Log the user viewing this ad
        UserAdView.objects.create(user=request.user, ad=next_ad)

        # Add points to the user's wallet
        wallet = (
            request.user.wallet
        )  # Assuming the user has a one-to-one relationship with Wallet
        wallet.add_points(5)  # Add 5 points to the wallet
        wallet.save()  # Save the updated wallet

        # Render the ad view page with the next ad
        return render(request, "ad_view.html", {"ad": next_ad})

    # If no more ads are available today, show the limit reached page
    return render(request, "limit_reached.html")




# ads countity area for user
@login_required
def available_ads(request):
    videos = Ad.objects.all()  # Get all videos uploaded by admin
    return render(request, "available_ads.html", {"videos": videos})



# add reference are for user
@login_required
def add_reference(request):
    # Fetch the user's references
    user_references = Reference.objects.filter(
        user=request.user
    )  # Get all references the user has added

    # Check if the user already has 3 references
    if user_references.count() >= 3:
        form_disabled = True
        form = None  # No need to show form if 3 references already added
        error = "You have already added the maximum number of references (3)."
    else:
        form_disabled = False
        error = None

        if request.method == "POST":
            form = ReferenceForm(request.POST)
            if form.is_valid():
                reference_id = form.cleaned_data.get("reference_id")
                try:
                    referred_user = User.objects.get(unique_id=reference_id)

                    # Condition 1: The user cannot refer themselves
                    if referred_user == request.user:
                        raise ValueError("You cannot refer yourself.")

                    # Condition 2: Check if the unique_id has already been used as a reference
                    if Reference.objects.filter(referred_user=referred_user).exists():
                        raise ValueError(
                            "This reference ID has already been used by another user."
                        )

                    # Add the reference
                    Reference.objects.create(
                        user=request.user, referred_user=referred_user
                    )

                except User.DoesNotExist:
                    error = "Invalid reference ID"
                except ValueError as e:
                    error = str(e)

                # Redirect to avoid form resubmission
                if not error:
                    return redirect("add_reference")
        else:
            form = ReferenceForm()

    # Pass the form, user's references, and the form_disabled flag to the template
    return render(
        request,
        "reference.html",
        {
            "form": form,
            "user_references": user_references,
            "error": error,
            "form_disabled": form_disabled,
        },
    )




# withdrawal area for user
@login_required
def withdrawal(request):
    wallet = (
        request.user.wallet
    )  # Assuming there is a one-to-one relationship with Wallet

    # Check if the user has at least 440 points
    if wallet.points < 440:
        form = None  # Do not show the form if points are less than 440
        message = "You need a minimum of 440 points to make a withdrawal."
    else:
        form = WithdrawalForm(request.POST or None)
        message = None
        if request.method == "POST" and form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.user = request.user
            withdrawal.status = "pending"
            withdrawal.save()

            # Deduct points from the wallet
            wallet.points -= withdrawal.amount
            wallet.save()

            return redirect("withdraw_points")

    # Get the user's withdrawal history
    withdrawal_history = Withdrawal.objects.filter(user=request.user)

    context = {
        "form": form,
        "message": message,
        "wallet_points": wallet.points,
        "withdrawal_history": withdrawal_history,
    }

    return render(request, "withdrawal.html", context)


 
 
# Check if the user is an admin
def is_superuser(user):
    return user.is_superuser



# user list for admin
@user_passes_test(is_superuser)
def admin_user_list(request):
    users = User.objects.all()

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user = User.objects.get(id=user_id)

        # Check if the admin is updating the status
        if "status" in request.POST:
            new_status = request.POST.get("status")
            user.status = new_status
            user.save()
        else:
            # Handle user deletion
            user.delete()
        return redirect("admin_user_list")

    return render(request, "admin/admin_user_list.html", {"users": users})




#  video uploading for admin
@user_passes_test(is_superuser)
def admin_video_upload(request):
    if request.method == "POST":
        form = VideoForm(
            request.POST, request.FILES
        )  # Ensure you handle both POST and FILES
        if form.is_valid():
            form.save()
            return redirect("admin_video_list")  # Redirect after successful upload
        else:
            print(form.errors)
    else:
        form = VideoForm()

    return render(request, "admin/admin_video_upload.html", {"form": form})




# total video list check for admin
@user_passes_test(is_superuser)
def admin_video_list(request):
    videos = Ad.objects.all()
    if request.method == "POST":
        video_id = request.POST.get("video_id")
        video = Ad.objects.get(id=video_id)
        video.delete()
        return redirect("admin_video_list")

    return render(request, "admin/admin_video_list.html", {"videos": videos})




# send notification area for admin
@user_passes_test(is_superuser)
def admin_send_notification(request):
    if request.method == "POST":
        message = request.POST.get("message")
        Notification.objects.create(message=message)
        return redirect("admin_send_notification")

    return render(request, "admin/admin_send_notification.html")





# notificantio list for admin 
@user_passes_test(is_superuser)
def admin_send_notification_list(request):
    notifications = Notification.objects.all()
    if request.method == "POST":
        notification_id = request.POST.get("notification_id")
        notification = Notification.objects.get(id=notification_id)
        notification.delete()
        return redirect("admin_send_notification_list")

    return render(
        request,
        "admin/admin_send_notification_list.html",
        {"notifications": notifications},
    )





# withdrawal list for admin
@user_passes_test(is_superuser)
def admin_withdrawal_view(request):
    # Get the status filter from the request (pending, processing, completed, canceled)
    status_filter = request.GET.get("status_filter")

    # Base queryset for withdrawals
    withdrawals = Withdrawal.objects.all()

    # Apply status filters
    if status_filter:
        withdrawals = withdrawals.filter(status=status_filter)

    # Handle status update via POST
    if request.method == "POST":
        withdrawal_id = request.POST.get("withdrawal_id")
        new_status = request.POST.get("new_status")
        withdrawal = Withdrawal.objects.get(id=withdrawal_id)
        withdrawal.status = new_status
        withdrawal.save()
        return redirect("admin_withdrawal_view")

    context = {
        "withdrawals": withdrawals,
        "status_filter": status_filter,
    }
    return render(request, "admin/admin_withdrawal.html", context)


