from django.contrib import admin
from .models import Quest, Report, Review, Tag, QuestCompletion, Ticket, TicketIssuance

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('id', 'name')

@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location', 'reward', 'date_created')
    search_fields = ('id', 'title', 'location', 'reward')
    list_filter = ('date_created', 'tags')
    filter_horizontal = ('tags',)

@admin.register(QuestCompletion)
class QuestCompletionAdmin(admin.ModelAdmin):
    list_display = ('user', 'quest', 'completion_date')
    search_fields = ('user__username', 'quest__title')
    list_filter = ('completion_date',)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'link', 'level')
    search_fields = ('title', 'description', 'link', 'level')

@admin.register(TicketIssuance)
class TicketIssuanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ticket', 'issue_date', 'used')
    search_fields = ('id', 'user__username', 'ticket__title')
    list_filter = ('issue_date', 'used')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('quest', 'user', 'rating', 'created_at')
    search_fields = ('quest__title', 'user__username', 'rating')
    list_filter = ('rating', 'created_at')
    
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'report_date', 'content')
    search_fields = ('user__username', 'content')
    list_filter = ('report_date',)