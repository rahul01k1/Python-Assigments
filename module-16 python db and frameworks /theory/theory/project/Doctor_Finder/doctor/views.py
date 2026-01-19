from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .utils.emails import send_appointment_email

from .models import UserProfile, Doctor, Appointment, ContactMessage
from .utils.emails import send_appointment_email


# =========================
# HOME PAGE
# =========================
def home(request):
    doctors = Doctor.objects.filter(
        is_verified=True,
        is_available=True
    ).order_by("-created_at")[:8]

    return render(request, "pages/home.html", {"doctors": doctors})


# =========================
# DOCTOR LIST
# =========================
def doctor_list(request):
    doctors = Doctor.objects.filter(
        is_verified=True,
        is_available=True
    ).order_by("-created_at")

    return render(request, "doctors/doctor_list.html", {"doctors": doctors})


# =========================
# PATIENT DASHBOARD
# =========================
@login_required
def patient_dashboard(request):
    if request.user.profile.role != "patient":
        return redirect("doctor:home")

    appointments = Appointment.objects.filter(
        patient=request.user
    ).select_related("doctor").order_by("-created_at")

    return render(
        request,
        "patient/dashboard.html",
        {"appointments": appointments}
    )


# =========================
# DOCTOR DASHBOARD
# =========================
@login_required
def doctor_dashboard(request):
    if request.user.profile.role != "doctor":
        return redirect("doctor:home")

    appointments = Appointment.objects.filter(
        doctor__user=request.user
    ).select_related("patient").order_by("-created_at")

    return render(
        request,
        "doctors/doctor_dashboard.html",
        {"appointments": appointments}
    )


# =========================
# APPROVE / REJECT APPOINTMENT
# =========================
@login_required
def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user != appointment.doctor.user:
        return redirect("doctor:home")

    appointment.status = "approved"
    appointment.save()

    # 📧 EMAIL NOTIFICATION
    send_appointment_email(
        subject="Appointment Approved | Leven Health",
        text_message=(
            f"Hello {appointment.patient.username},\n\n"
            f"Your appointment with Dr. {appointment.doctor.full_name} "
            f"has been approved.\n\n"
            f"Date: {appointment.appointment_date}\n"
            f"Time: {appointment.appointment_time}\n\n"
            "Regards,\nLeven Health"
        ),
        recipient_list=[appointment.patient.email],
    )

    return redirect("doctor:doctor_dashboard")



@login_required
def reject_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user != appointment.doctor.user:
        return redirect("doctor:home")

    appointment.status = "rejected"
    appointment.save()

    send_appointment_email(
        subject="Appointment Rejected – Leven Health",
        text_message=(
            f"Hi {appointment.patient.username},\n\n"
            f"Unfortunately, your appointment with "
            f"Dr. {appointment.doctor.full_name} was rejected.\n\n"
            "Leven Health Team"
        ),
        recipient_list=[appointment.patient.email],
    )

    messages.info(request, "Appointment rejected.")
    return redirect("doctor:doctor_dashboard")


# =========================
# PROFILE VIEW / UPDATE
# =========================
@login_required
def profile_view(request):
    return render(request, "patient/profile.html")


@login_required
def profile_update(request):
    user = request.user
    profile = user.profile

    if request.method == "POST":
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        profile.phone = request.POST.get("phone")

        if request.FILES.get("profile_image"):
            profile.profile_image = request.FILES["profile_image"]

        user.save()
        profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("doctor:profile")

    return render(request, "patient/profile_edit.html")


# =========================
# DOCTOR PROFILE (PUBLIC)
# =========================
def doctor_profile(request, doctor_id):
    doctor = get_object_or_404(
        Doctor,
        id=doctor_id,
        is_verified=True,
        is_available=True
    )

    return render(request, "doctors/doctor_profile.html", {"doctor": doctor})


# =========================
# BOOK APPOINTMENT
# =========================
@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id, is_available=True)

    if request.method == "POST":
        date = request.POST.get("date")
        time = request.POST.get("time")
        reason = request.POST.get("reason", "")

        if not date or not time:
            messages.error(request, "Please select date and time.")
            return redirect("doctor:book_appointment", doctor_id=doctor.id) #type:ignore

        appointment = Appointment.objects.create(
            patient=request.user,
            doctor=doctor,
            appointment_date=date,
            appointment_time=time,
            reason=reason
        )

        # 📧 EMAIL TO PATIENT
        send_appointment_email(
            subject="Appointment Booked | Leven Health",
            text_message=(
                f"Hello {request.user.username},\n\n"
                f"Your appointment with Dr. {doctor.full_name} has been booked.\n"
                f"Date: {date}\n"
                f"Time: {time}\n\n"
                "Thank you,\nLeven Health"
            ),
            recipient_list=[request.user.email]
        )

        messages.success(request, "Appointment booked successfully.")
        return redirect("doctor:my_appointments")

    return render(request, "appointments/book_appointment.html", {"doctor": doctor})


# =========================
# MY APPOINTMENTS
# =========================
@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(
        patient=request.user
    ).select_related("doctor").order_by("-created_at")

    return render(
        request,
        "appointments/my_appointments.html",
        {"appointments": appointments}
    )


# =========================
# AUTH
# =========================
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("doctor:signup")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        UserProfile.objects.create(user=user, role="patient")

        messages.success(request, "Account created successfully.")
        return redirect("doctor:login")

    return render(request, "accounts/signup.html")


def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )

        if user:
            login(request, user)
            return redirect(
                "doctor:doctor_dashboard"
                if user.profile.role == "doctor" #type:ignore
                else "doctor:home"
            )

        messages.error(request, "Invalid credentials.")

    return render(request, "accounts/login.html")


@require_POST
def logout_view(request):
    logout(request)
    return redirect("doctor:login")


# =========================
# STATIC PAGES
# =========================
def services_page(request):
    return render(request, "pages/services.html")


def about_page(request):
    return render(request, "pages/about.html")

def doctor_detail(request, id):
    doctor = get_object_or_404(
        Doctor,
        id=id,
        is_verified=True,
        is_available=True
    )

    return render(
        request,
        "doctors/doctor_detail.html",
        {
            "doctor": doctor
        }
    )


def contact_page(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            name = request.user.get_full_name() or request.user.username
            email = request.user.email
        else:
            name = request.POST.get("name")
            email = request.POST.get("email")

        message_text = request.POST.get("message")

        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message_text
        )

        messages.success(request, "Thank you! Your message has been sent.")
        return redirect("doctor:contact")

    return render(request, "pages/contact.html")

