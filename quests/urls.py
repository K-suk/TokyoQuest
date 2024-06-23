# quests/urls.py
from django.urls import path
from . import views

app_name = "quests"

urlpatterns = [
    path('quest_list', views.QuestListView.as_view(), name='quest_list'),
    path('quest/<int:pk>/', views.quest_detail, name='quest_detail'),
    path('complete_quest/<int:quest_id>/', views.complete_quest, name='complete_quest'),
    path('ticket_list/', views.TicketListView.as_view(), name='ticket_list'),
    path('claim_ticket/<int:ticket_id>/', views.claim_ticket, name='claim_ticket'),
    path('use_ticket/<int:issuance_id>/', views.use_ticket, name='use_ticket'),
    path('quest/<int:quest_id>/add_review/', views.add_review, name='add_review'),
]
