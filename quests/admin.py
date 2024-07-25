from django.contrib import admin
from .models import Quest, Report, Review, SavedQuest, Tag, QuestCompletion, Ticket, TicketIssuance, TravelPlan
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('id', 'name')

@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location', 'badget', 'date_created', 'imgUrl', 'exampleUrl')
    search_fields = ('id', 'title', 'location', 'badget')
    list_filter = ('date_created', 'tags')
    filter_horizontal = ('tags',)

@admin.register(QuestCompletion)
class QuestCompletionAdmin(admin.ModelAdmin):
    list_display = ('user', 'quest', 'completion_date', 'media')
    search_fields = ('user__username', 'quest__title')
    list_filter = ('completion_date',)

@admin.register(TravelPlan)
class TravelPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_created')
    search_fields = ('user__username',)
    filter_horizontal = ('quests',)  # quests の管理に多対多フィールド用のウィジェットを使用

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user').prefetch_related('quests')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'link', 'level', 'issued_to_users')
    search_fields = ('title', 'description', 'link', 'level')

    def issued_to_users(self, obj):
        return ", ".join([user.account_id for user in obj.issued_to.all()])
    issued_to_users.short_description = 'Issued To'

@admin.register(TicketIssuance)
class TicketIssuanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ticket', 'issue_date', 'used')
    search_fields = ('id', 'user__account_id', 'ticket__title')
    list_filter = ('issue_date', 'used')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('quest', 'user', 'rating', 'created_at')
    search_fields = ('quest__title', 'user__account_id', 'rating')
    list_filter = ('rating', 'created_at')
    
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'report_date', 'content')
    search_fields = ('user__account_id', 'content')
    list_filter = ('report_date',)

@admin.register(SavedQuest)
class SavedQuestAdmin(admin.ModelAdmin):
    list_display = ('user', 'quest', 'saved_at')
    search_fields = ('user__email', 'quest__title')
    list_filter = ('saved_at',)