# # tokyoquest/middleware.py
# from django.shortcuts import redirect
# from django.urls import reverse

# class CheckUserDoneMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)

#         if request.user.is_authenticated and request.user.done:
#             reports_url = reverse('quests:report_view')
#             logout_url = reverse('accounts:logout')
#             if not request.path.startswith(reports_url) and request.path != logout_url:
#                 return redirect(reports_url)

#         return response

# tokyoquest/middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class CheckUserDoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.done:
            reports_url = reverse('quests:report_view')
            logout_url = reverse('accounts:logout')  # ログアウトURLはそのまま
            if not request.path.startswith(reports_url) and request.path != logout_url:
                return redirect(reports_url)

        response = self.get_response(request)
        return response
