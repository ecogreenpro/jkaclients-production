import random

from django.contrib import messages, auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from account.models import Invoice
from authentication.froms import ProfileUpdateForm
from authentication.models import Profile, Team
from jkaclients import settings
from service.models import MyService, Contract


def get_substring_before_at(email):
    parts = email.split('@')
    if len(parts) >= 2:
        return parts[0]
    else:
        return None


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('authentication:dashboard')
    else:
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            username = get_substring_before_at(email)
            password = request.POST.get('password')
            check_user = User.objects.filter(username=username).first()
            check_profile = Profile.objects.filter(user__email=email).first()

            if check_user:
                messages.error(request, '<strong>The username already taken.</strong>')
                return redirect('authentication:sign_up')
            if check_profile:
                messages.error(request, '<strong>The email already taken.</strong>')
                return redirect('authentication:sign_up')
            else:
                user = User.objects.create_user(username=username, email=email, first_name=first_name,
                                                last_name=last_name,
                                                password=password)
                user.is_staff = False
                user.is_active = False
                user.save()
                otp = str(random.randint(100000, 999999))
                profile = Profile(user=user, phone=phone, otp=otp)
                profile.save()
                request.session['email'] = email
                email_context = {
                    'full_name': first_name + ' ' + last_name,
                    'otp': otp,
                    'username': username
                }
                subject = 'Verify your new JK Associates Clients Portal'
                from_email = 'JK Associates <noreply@jkassociates.com.bd>'
                to_email = [email]
                text_content = f'Verify your new  account. OTP - {otp}'
                template = get_template('emails/account_confirmation.html').render(email_context)
                mail = EmailMultiAlternatives(subject, text_content, from_email, to_email)
                mail.attach_alternative(template, "text/html")
                mail.send()
                messages.success(request, f'OTP Code has been sent to <strong>{email}</strong>')
                return redirect('authentication:otp_verify')
    return render(request, 'authentication/sign_up.html')


def otp_verify(request):
    if 'email' in request.session:
        email = request.session['email']
        if request.method == 'POST':
            otp = request.POST.get('otp')
            profile = Profile.objects.filter(user__email=email).first()
            user = User.objects.get(id=profile.user.id)
            if otp == profile.otp:
                if profile.user.email and profile.phone:
                    user.is_active = True
                    profile.is_verify = True
                    user.save()
                    profile.save()
                    auth.login(request, user)
                    return redirect('authentication:dashboard')
                else:
                    auth.login(request, user)
                    return redirect('client:profile_setting')
            else:
                messages.error(request, 'Invalid OTP')
                return render(request, 'authentication/verify-otp.html')
    else:
        return redirect('authentication:login')
    return render(request, 'authentication/verify-otp.html')


def resend_otp(request):
    if 'email' in request.session:
        email = request.session['email']
        otp = str(random.randint(100000, 999999))
        profile = Profile.objects.filter(user__email=email).first()
        user = User.objects.get(id=profile.user.id)
        profile.otp = otp
        profile.save()
        email_context = {
            'full_name': user.get_full_name,
            'otp': otp,
            'username': user.username
        }
        subject = 'Verify your new JK Associates Clients Portal'
        from_email = 'JK Associates <noreply@jkassociates.com.bd>'
        to_email = [user.email]
        text_content = f'Verify your new  account. OTP - {otp}'
        template = get_template('emails/account_confirmation.html').render(email_context)
        mail = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        mail.attach_alternative(template, "text/html")
        mail.send()
        request.session['email'] = email
        messages.success(request, f'OTP Code has been sent again to <strong>{email}</strong>')
        return redirect('authentication:otp_verify')
    else:
        return redirect('authentication:login')


def login(request):
    if request.user.is_authenticated:
        return redirect('authentication:dashboard')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            check_user = User.objects.filter(email=email).first()
            check_profile = Profile.objects.filter(user__email=email).first()
            if check_user or check_profile:
                profile = Profile.objects.get(user__email=email)
                user = auth.authenticate(username=profile.user.username, password=password)
                if User.objects.filter(username=profile.user.username, is_active=False):
                    messages.error(request,
                                   f'Account is not active yet, verify your mobile number. '
                                   f'OTP Code has been sent to <strong>{email}</strong>')
                    request.session['email'] = email
                    return redirect('authentication:otp_verify')
                else:
                    if user is not None:
                        if check_user.email and check_profile.phone:
                            auth.login(request, user)
                            return redirect('authentication:dashboard')
                        else:
                            auth.login(request, user)
                            return redirect('client:profile_setting')
                    else:
                        messages.error(request, 'Invalid Credentials, incorrect password.')
                        return redirect('authentication:login')
            else:
                messages.error(request, 'Invalid Credentials, <strong>there no account with this username.</strong>')
                return redirect('authentication:login')
        else:
            return render(request, 'authentication/login.html')


@login_required(login_url='/')
def logout(request):
    auth.logout(request)
    messages.info(request, 'Logged out Successfully ')
    return redirect('authentication:login')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        check_user = User.objects.filter(email=email).first()
        check_profile = Profile.objects.filter(user__email=email).first()
        if check_user or check_profile:
            otp = str(random.randint(100000, 999999))
            profile = Profile.objects.filter(user__email=email).first()
            user = User.objects.get(id=profile.user.id)
            profile.otp = otp
            profile.save()
            email_context = {
                'full_name': user.get_full_name,
                'otp': otp,
                'username': user.username
            }
            subject = 'Verify your Password Recovery for JK Associates Clients Portal'
            from_email = 'JK Associates <noreply@jkassociates.com.bd>'
            to_email = [user.email]
            text_content = f'Verify your new Amazon account. OTP - {otp}'
            template = get_template('emails/account_confirmation.html').render(email_context)
            mail = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            mail.attach_alternative(template, "text/html")
            mail.send()
            request.session['email'] = email
            messages.success(request, f'OTP Code has been sent to <strong>{email}</strong>')
            return redirect('authentication:recover_password_otp_verify')
        else:
            messages.error(request, 'Invalid Credentials, <strong>there no account with this email.</strong>')
            return redirect('authentication:forgot_password')

    return render(request, 'authentication/forgot-password.html')


def recover_password_otp_verify(request):
    if 'email' in request.session:
        email = request.session['email']
        if request.method == 'POST':
            otp = request.POST.get('otp')
            profile = Profile.objects.filter(user__email=email).first()
            if otp == profile.otp:
                user = User.objects.get(id=profile.user.id)
                uid = str(urlsafe_base64_encode(force_bytes(user.pk)))
                token = str(default_token_generator.make_token(user))
                return redirect('/forgot-password/' + uid + '/' + token + '/')
            else:
                messages.error(request, 'Invalid OTP')
                return render(request, 'authentication/forgot-password-verify-otp.html')
    else:
        return redirect('authentication:login')
    return render(request, 'authentication/forgot-password-verify-otp.html')


def recover_password_resend_otp(request):
    if 'email' in request.session:
        email = request.session['email']
        otp = str(random.randint(100000, 999999))
        profile = Profile.objects.filter(user__email=email).first()
        user = User.objects.get(id=profile.user.id)
        profile.otp = otp
        profile.save()
        email_context = {
            'full_name': user.get_full_name,
            'otp': otp,
            'username': user.username
        }
        subject = 'Verify your Password Recovery for JK Associates Clients Portal'
        from_email = 'JK Associates <noreply@jkassociates.com.bd>'
        to_email = [user.email]
        text_content = f'Verify your new  account. OTP - {otp}'
        template = get_template('emails/account_confirmation.html').render(email_context)
        mail = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        mail.attach_alternative(template, "text/html")
        mail.send()
        request.session['email'] = email
        messages.success(request, f'OTP Code has been sent again to <strong>{email}</strong>')
        return redirect('authentication:recover_password_otp_verify')
    else:
        return redirect('authentication:login')


@login_required(login_url='/')
def account_settings(request):
    form = PasswordChangeForm(request.user)
    return render(request, 'authentication/account-settings.html', {'form': form})


@login_required(login_url='/')
def account_update(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        user = User.objects.get(username=request.user.username)
        if profile_form.is_valid():
            if first_name:
                user.first_name = first_name
                user.save()
            if last_name:
                user.last_name = last_name
                user.save()
            profile_form.save()
            messages.info(request, 'Profile Updated Successfully')
            current_site = get_current_site(request)
            mail_context = {
                'user': request.user,
                'domain': current_site.domain,
            }
            subject = f'Hello! {request.user.get_full_name()} you update your Personal information'
            content = f'Hello! {request.user.get_full_name()} you update your Personal information'
            from_email = 'JK Associates <noreply@jkassociates.com.bd>'
            to_email = [request.user.email]
            templates = get_template('emails/account_update.html').render(mail_context)
            mail = EmailMultiAlternatives(subject, content, from_email, to_email)
            mail.attach_alternative(templates, 'text/html')
            mail.send()
        return redirect('authentication:account_settings')
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        user = User.objects.get(username=request.user.username)
        context = {
            'profile_form': profile_form,
            'user': user
        }
        return render(request, 'authentication/account-update.html', context)


@login_required(login_url='/')
def account_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('authentication:account_settings')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return redirect('authentication:account_settings')
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'authentication/account-settings.html', {'form': form})


@login_required(login_url='/')
def dashboard(request):
    count_service_ongoing = MyService.objects.filter(user=request.user, my_service_status=False).count()
    count_service_complete = MyService.objects.filter(user=request.user, my_service_status=True).count()
    invoice_amount = Contract.objects.filter(user=request.user).aggregate(Sum('total_amount_of_contract'))
    payment_amount = Invoice.objects.filter(user=request.user).aggregate(Sum('payment_received_amount'))
    due_amount = Invoice.objects.filter(user=request.user).aggregate(Sum('due_amount'))

    context = {
        'count_service_ongoing': count_service_ongoing,
        'count_service_complete': count_service_complete,
        'invoice_amount': invoice_amount,
        'payment_amount': payment_amount,
        'due_amount': due_amount,
    }
    return render(request, 'authentication/dashboard.html', context)


@login_required(login_url='/')
def my_team(request):
    teams = Team.objects.filter(user=request.user)

    context = {
        'teams': teams
    }
    return render(request, 'authentication/my-team.html', context)
