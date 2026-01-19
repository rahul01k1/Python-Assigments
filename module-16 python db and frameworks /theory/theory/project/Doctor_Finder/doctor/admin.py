from django.contrib import admin
from .models import UserProfile , Doctor , Appointment , ContactMessage


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'is_verified')
    search_fields = ('user__username', 'user__email')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'specialization',
        'experience_years',
        'consultation_fee',
        'is_available',
        'is_verified'
    )
    search_fields = ('full_name', 'specialization')
    list_filter = ('specialization', 'is_verified', 'is_available')



@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient",
        "doctor",
        "appointment_date",
        "appointment_time",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "appointment_date",
        "doctor",
    )

    search_fields = (
        "patient__username",
        "doctor__full_name",
    )

    ordering = ("-created_at",)

    readonly_fields = ("created_at",)

    fieldsets = (
        ("Appointment Info", {
            "fields": (
                "patient",
                "doctor",
                "appointment_date",
                "appointment_time",
            )
        }),
        ("Status", {
            "fields": ("status",)
        }),
        ("Notes", {
            "fields": ("notes",)
        }),
        ("Metadata", {
            "fields": ("created_at",)
        }),
    )

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email")