from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from videos.models import Video
from mpesa.models import Transaction
from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncHour

""" import the forms from forms to create the views"""
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm


def register(request):
    """create a view for the user registration form"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Account succcessfully created for {username}!')
            return redirect('login')
        else:
            messages.warning(request, "To err is human")

    else:
        form = UserRegisterForm()

    """pass form as the context of the form filled/empty"""
    return render(
        request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """Create view for the profile update form
    Returns:
        form: form data to access in the template
    """
    if request.method == 'POST':
        u_update = UserUpdateForm(request.POST, instance=request.user)
        p_update = ProfileUpdateForm(request.POST, request.FILES,
                                     instance=request.user.profile)
        if u_update.is_valid() and p_update.is_valid():
            u_update.save()
            p_update.save()
            messages.success(request, f'Account succcessfully updated!')
            return redirect('profile')
        else:
            context = {'u_form': u_update, 'p_form': p_update, }
            # messages.warning(request, f'Error!')
            return render(request, 'users/profile.html', context)
    else:
        u_update = UserUpdateForm(instance=request.user)
        p_update = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'u_form': u_update,
            'p_form': p_update,
        }  # varriables to access in the template

        return render(request, 'users/profile.html', context)


@login_required
def dashboard(request):
    """view for the client dashboard to Get transaction-related information

    Returns:
        context data:
        unique_ip_count,
        total_revenue,
        total_transactions,
        avg_transaction_amount,
        transaction_hour
    """
    user = request.user
    videos = Video.objects.filter(user=user)

    transaction_info = Transaction.objects.filter(
        video__in=videos, status='successful').aggregate(
        total_revenue=Sum('amount'),
        total_transactions=Count('id'),
        unique_ip_count=Count('ip', distinct=True)
    )
    avg_transaction_amount = Transaction.objects.filter(
        video__in=videos, status='successful').aggregate(
            avg_transaction_amount=Avg('amount'))['avg_transaction_amount']

    transaction_hours = Transaction.objects.filter(
        video__in=videos, status='successful').annotate(
            transaction_hour=TruncHour('created')).values(
                'transaction_hour').annotate(
                transaction_count=Count('id')).order_by(
                    '-transaction_count')[:5]

    context = {
        'user': user,
        'videos': videos,
        'avg_transaction_amount': avg_transaction_amount,
        'transaction_info': transaction_info,
        'transaction_hours': transaction_hours,
    }

    return render(request, 'users/dashboard.html', context)
