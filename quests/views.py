from django.shortcuts import redirect, render, get_object_or_404

from accounts.models import User
from .forms import ReviewForm, TagSearchForm
from .models import Quest, QuestCompletion, Report, Ticket, TicketIssuance
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler

class QuestListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = TagSearchForm(request.GET)
        completed_quests = QuestCompletion.objects.filter(user=request.user).values_list('quest', flat=True)
        quests = Quest.objects.exclude(id__in=completed_quests)
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            if keyword:
                quests = quests.filter(tags__name__icontains=keyword)
        return render(request, 'quests/quest_list.html', {'quests': quests, 'form': form})

def quest_detail(request, pk):
    quest = get_object_or_404(Quest, pk=pk)
    reviews = quest.reviews.all()
    return render(request, 'quests/quest_detail.html', {'quest': quest, 'reviews': reviews})

@login_required
def complete_quest(request, quest_id):
    user = User.objects.get(id=request.user.id)
    user.level += 1
    user.save()
    quest = get_object_or_404(Quest, id=quest_id)
    done_quest = QuestCompletion.objects.create(
        user=request.user,
        quest=quest,
    )
    done_quest.save()
    return redirect('quests:quest_list')

class TicketListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tickets = Ticket.objects.all()
        return render(request, 'quests/ticket_list.html', {'tickets': tickets})
    
@login_required
def use_ticket(request, issuance_id):
    ticket = get_object_or_404(TicketIssuance, id=issuance_id)
    ticket.used = True
    ticket.save()
    return redirect('accounts:profile')

@login_required
def claim_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket_issuance = TicketIssuance.objects.create(
        user=request.user,
        ticket=ticket
    )
    return redirect('accounts:profile')

@login_required
def add_review(request, quest_id):
    quest = get_object_or_404(Quest, id=quest_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.quest = quest
            review.save()
            return redirect('quests:quest_detail', pk=quest_id)
    else:
        form = ReviewForm()
    return render(request, 'quests/add_review.html', {'form': form, 'quest': quest})

def handle():
    now = timezone.now()
    users = User.objects.filter(due__lt=now, done=False)

    for user in users:
        user.done = True
        user.save()

        report_content = generate_report_content(user)
        Report.objects.create(user=user, content=report_content)

def generate_report_content(user):
    completed_quests = QuestCompletion.objects.filter(user=user)
    report_content = f'Report for {user.first_name} {user.last_name}:\n\n'
    report_content += f'Completed Quests:\n'
    for completion in completed_quests:
        report_content += f'- {completion.quest.title} (Completed on {completion.completion_date})\n'
    return report_content


def start():
    scheduler = BackgroundScheduler()

    scheduler.add_job(handle, 'interval', seconds=12) # schedule
    scheduler.start()