from django.contrib import admin
from .models import Proposal

@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ('fio', 'email', 'phone', 'created_at', 'is_checked')
    list_filter = ('created_at', 'is_checked')
    search_fields = ('fio', 'email', 'phone')
    readonly_fields = ('created_at',)