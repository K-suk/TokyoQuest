# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    QuestViewSet, generate_report, get_user_travel_plan, report_view, quest_detail, complete_quest, 
    TicketViewSet, save_quest, is_quest_saved, get_saved_quests, search_quests_by_tag, 
    use_ticket, claim_ticket, add_review, get_incomplete_quests, get_ticket_issuances, 
    get_reviews, get_completed_quests, create_travel_plan, get_reports
)

router = DefaultRouter()
router.register(r'quests', QuestViewSet, basename='quest')
router.register(r'tickets', TicketViewSet, basename='ticket')

app_name = "quests"

urlpatterns = [
    path('quests/reports/', report_view, name='report_view'),
    path('quests/incomplete/', get_incomplete_quests, name='get_incomplete_quests'),
    path('quests/search/', search_quests_by_tag, name='search_quests_by_tag'),
    path('quests/saved/', get_saved_quests, name='get_saved_quests'),
    path('', include(router.urls)),
    path('quests/<int:pk>/', quest_detail, name='quest_detail'),
    path('quests/<int:quest_id>/complete/', complete_quest, name='complete_quest'),
    path('quests/<int:quest_id>/save/', save_quest, name='save_quest'),
    path('quests/<int:quest_id>/is_saved/', is_quest_saved, name='is_quest_saved'),
    path('tickets/<int:issuance_id>/use/', use_ticket, name='use_ticket'),
    path('tickets/<int:ticket_id>/claim/', claim_ticket, name='claim_ticket'),
    path('quests/<int:quest_id>/reviews/add/', add_review, name='add_review'),
    path('quests/<int:quest_id>/reviews/', get_reviews, name='get_reviews'),
    path('tickets/<int:ticket_id>/issuances/', get_ticket_issuances, name='get_ticket_issuances'),
    path('completed-quests/', get_completed_quests, name='completed-quests'),
    path('travel-plans/create_plan/', create_travel_plan, name='create_travel_plan'),
    path('travel-plans/', get_user_travel_plan, name='get_user_travel_plan'),
    path('generate_report/', generate_report, name='generate_report'),
    path('reports/', get_reports, name='get_reports'),
]