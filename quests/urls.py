from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    QuestViewSet, quest_detail, complete_quest, 
    TicketViewSet, use_ticket, claim_ticket, add_review, 
    get_incomplete_quests, get_ticket_issuances, get_reviews
)

router = DefaultRouter()
router.register(r'quests', QuestViewSet, basename='quest')
router.register(r'tickets', TicketViewSet, basename='ticket')

app_name = "quests"

urlpatterns = [
    path('quests/incomplete/', get_incomplete_quests, name='get_incomplete_quests'),
    path('', include(router.urls)),
    path('quests/<int:pk>/', quest_detail, name='quest_detail'),
    path('quests/<int:quest_id>/complete/', complete_quest, name='complete_quest'),
    path('tickets/<int:issuance_id>/use/', use_ticket, name='use_ticket'),
    path('tickets/<int:ticket_id>/claim/', claim_ticket, name='claim_ticket'),
    path('quests/<int:quest_id>/reviews/add/', add_review, name='add_review'),
    path('quests/<int:quest_id>/reviews/', get_reviews, name='get_reviews'),
    path('tickets/<int:ticket_id>/issuances/', get_ticket_issuances, name='get_ticket_issuances'),
]
