from datetime import timedelta

from django.contrib import admin
from django.utils import timezone

from .models import Appointment


# ---------- Inline utilisé dans la fiche Patient (AccountApp/admin.py) ----------
class AppointmentInline(admin.StackedInline):
    model = Appointment
    extra = 0
    fields = ('doctor', 'appointment_date', 'duration_minutes', 'status', 'reason', 'prescription')
    ordering = ('-appointment_date',)


# ---------- Filtre personnalisé sur la date ----------
class DateRangeFilter(admin.SimpleListFilter):
    title = "période"
    parameter_name = "periode"

    def lookups(self, request, model_admin):
        return (
            ('today', "Aujourd'hui"),
            ('week', "Cette semaine"),
            ('upcoming', "À venir"),
        )

    def queryset(self, request, queryset):
        today = timezone.localdate()
        if self.value() == 'today':
            return queryset.filter(appointment_date__date=today)
        if self.value() == 'week':
            start = today - timedelta(days=today.weekday())  # lundi
            end = start + timedelta(days=7)
            return queryset.filter(appointment_date__date__gte=start,
                                   appointment_date__date__lt=end)
        if self.value() == 'upcoming':
            return queryset.filter(appointment_date__gt=timezone.now())
        return queryset


# ---------- Admin Appointment ----------
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_date', 'doctor', 'patient', 'duration_minutes', 'status')
    list_filter = ('status', 'doctor', DateRangeFilter)
    search_fields = (
        'patient__last_name',
        'patient__national_id',
        'doctor__last_name',
        'doctor__license_number',
    )
    ordering = ('-appointment_date',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ("Participants", {"fields": ("doctor", "patient")}),
        ("Planification", {"fields": ("appointment_date", "duration_minutes", "status")}),
        ("Dossier", {"fields": ("reason", "prescription")}),
        ("Suivi", {"fields": ("created_at", "updated_at")}),
    )
    actions = ['confirm_appointments', 'cancel_appointments']

    @admin.action(description="Confirmer les rendez-vous sélectionnés")
    def confirm_appointments(self, request, queryset):
        updated = queryset.update(status=Appointment.Status.CONFIRMED)
        self.message_user(request, f"{updated} rendez-vous confirmé(s).")

    @admin.action(description="Annuler les rendez-vous sélectionnés")
    def cancel_appointments(self, request, queryset):
        updated = queryset.update(status=Appointment.Status.CANCELLED)
        self.message_user(request, f"{updated} rendez-vous annulé(s).")