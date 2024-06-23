from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import (LoginView as BaseLoginView, LogoutView as BaseLogoutView,
                                    PasswordChangeDoneView, PasswordChangeView, 
                                    PasswordResetView, PasswordResetDoneView, 
                                    PasswordResetConfirmView, PasswordResetCompleteView)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import User
from quests.models import Report, Ticket, TicketIssuance

from .forms import LoginFrom, ProfileForm
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required

class IndexView(TemplateView):
    """ ホームビュー """
    template_name = "index.html"
    
# ログインビューを作成
class LoginView(BaseLoginView):
    form_class = LoginFrom
    template_name = "accounts/login.html"
    
class LogoutView(BaseLogoutView):
    success_url = reverse_lazy("accounts:index")
    
class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    """パスワード変更ビュー"""
    success_url = reverse_lazy('accounts:password_change_done')
    template_name = 'accounts/password_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        context["form_name"] = "password_change"
        return context

class PasswordChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
    """パスワード変更完了"""
    template_name = 'accounts/password_change_done.html'
    
class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'accounts/mail_template/reset/subject.txt'
    email_template_name = 'accounts/mail_template/reset/message.txt'
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = self.request.scheme
        context['domain'] = self.request.get_host()
        return context

class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'accounts/password_reset_done.html'

class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'accounts/password_reset_confirm.html'

class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'accounts/password_reset_complete.html'
    
class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            user_data = User.objects.get(id=request.user.id)
        except ObjectDoesNotExist:
            return render(request, 'error.html', {'error': 'User does not exist'})
        issued_tickets = TicketIssuance.objects.filter(user=request.user).select_related('ticket')
        issued_ticket_ids = issued_tickets.values_list('ticket_id', flat=True)
        tickets = Ticket.objects.exclude(id__in=issued_ticket_ids)
        return render(request, 'accounts/profile.html', {
            'user_data': user_data,
            'issued_tickets': issued_tickets,
            'tickets': tickets
        })

class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            user_data = User.objects.get(id=request.user.id)
        except ObjectDoesNotExist:
            return render(request, 'error.html', {'error': 'User does not exist'})

        form = ProfileForm(
            initial={
                'first_name': user_data.first_name,
                'last_name': user_data.last_name,
                'contact_address': user_data.contact_address
            }
        )
        return render(request, 'accounts/profile_edit.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        try:
            user_data = User.objects.get(id=request.user.id)
        except ObjectDoesNotExist:
            return render(request, 'error.html', {'error': 'User does not exist'})

        form = ProfileForm(request.POST)
        if form.is_valid():
            user_data.first_name = form.cleaned_data['first_name']
            user_data.last_name = form.cleaned_data['last_name']
            user_data.contact_address = form.cleaned_data['contact_address']
            user_data.save()  # ここでユーザー情報を保存する
            return redirect('accounts:profile')
        return render(request, 'accounts/profile_edit.html', {
            'form': form
        })

@login_required
def user_reports(request):
    reports = Report.objects.filter(user=request.user)
    return render(request, 'accounts/reports.html', {'reports': reports})
