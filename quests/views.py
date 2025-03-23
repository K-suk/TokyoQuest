import random
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.shortcuts import get_object_or_404
from accounts.models import User
from .models import Quest, QuestCompletion, SavedQuest, Tag, Review, TravelPlan
from .serializers import QuestListSerializer, QuestDetailSerializer, QuestCompletionSerializer, SavedQuestSerializer, ReviewSerializer, TravelPlanSerializer
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from rest_framework import status
from django.db import transaction
import uuid
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import parser_classes, action
from django.db.models import Q

logger = logging.getLogger(__name__)

class QuestViewSet(viewsets.ModelViewSet):
    queryset = Quest.objects.prefetch_related('tags').all()
    def get_serializer_class(self):
        if self.action in ['list']:
            return QuestListSerializer
        return QuestDetailSerializer

# get all incompleted quests, avoiding having too much data in database instead of a little bit of increase in response time...(still pretty tiny tho)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_incomplete_quests(request):
    user = request.user
    try:
        completed_quests = set(QuestCompletion.objects.filter(user=user).values_list('quest_id', flat=True))
        incomplete_quests = Quest.objects.exclude(id__in=completed_quests).only('id', 'title', 'imgUrl')
        serializer = QuestListSerializer(incomplete_quests, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error fetching incomplete quests: {e}")
        return Response({'error': 'Error retrieving incomplete quests'}, status=500)

# get all completed quests
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_completed_quests(request):
    user = request.user
    completed_quests = QuestCompletion.objects.filter(user=user)
    serializer = QuestCompletionSerializer(completed_quests, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_tags(request):
    try:
        tags = Tag.objects.all()
        tag_list = [tag.name for tag in tags]
        logger.info(f"Retrieved {len(tag_list)} tags")
        return Response(tag_list)
    except Exception as e:
        logger.error(f"Error fetching tags: {e}")
        return Response({'error': 'Error retrieving tags'}, status=500)
    
# to search quest ここのシステム修正するかも
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_quests_by_tags(request):
    tag_names = request.query_params.get('tags')
    limit = request.query_params.get('limit')

    logger.info(f"Received tags: {tag_names}")
    logger.info(f"Received limit: {limit}")

    if not tag_names:
        logger.error("Tags not provided")
        return Response({'error': 'Tags not provided'}, status=400)

    try:
        tag_list = tag_names.split(',')
        logger.info(f"Parsed tags: {tag_list}")

        queryset = Quest.objects.filter(tags__name__in=tag_list).distinct()

        if limit:
            try:
                queryset = queryset[:int(limit)]
            except ValueError:
                logger.error("Invalid limit value")
                return Response({'error': 'Invalid limit value'}, status=400)

        serializer = QuestListSerializer(queryset, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error processing tags: {e}")
        return Response({'error': 'Error processing tags'}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_quests_by_tag(request):
    tag_name = request.query_params.get('tag')
    if not tag_name:
        logger.error("Tag not provided")
        return Response({'error': 'Tag not provided'}, status=400)
    
    logger.info(f"Received search request for tag: {tag_name}")
    
    quests = Quest.objects.filter(tags__name=tag_name).only('id', 'title', 'imgUrl').prefetch_related('tags')
    
    serializer = QuestListSerializer(quests, many=True)
    logger.info(f"Found quests: {len(quests)}")
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def quest_detail(request, pk):
    quest = get_object_or_404(Quest, pk=pk)
    serializer = QuestDetailSerializer(quest)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
@transaction.atomic
def complete_quest(request, quest_id):
    user = request.user
    quest = get_object_or_404(Quest, id=quest_id)
    
    if QuestCompletion.objects.filter(user=user, quest=quest).exists():
        print("Quest already completed")
        return Response({'status': 'quest already completed'}, status=status.HTTP_200_OK)
    
    try:
        # デバッグ用にリクエスト内容をprintで出力
        print(f"Request method: {request.method}")
        print(f"Request content-type: {request.content_type}")
        print(f"Request FILES: {request.FILES}")
        print(f"Request POST: {request.POST}")

        media_file = request.FILES.get('media')
        if not media_file:
            print("No media file provided")
            return Response({'status': 'error', 'detail': 'No media file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.level += 1
        user.save()
        done_quest = QuestCompletion.objects.create(user=user, quest=quest, media=media_file)
        print("Quest completed successfully")
        return Response({'status': 'quest completed'}, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error completing quest: {e}")
        return Response({'status': 'error', 'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request, quest_id):
    quest = get_object_or_404(Quest, id=quest_id)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, quest=quest)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reviews(request, quest_id):
    quest = get_object_or_404(Quest, id=quest_id)
    reviews = Review.objects.filter(quest=quest)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

# ここのアルゴリズムは絶対に修正しよう。
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_travel_plan(request):
    user = request.user
    area = request.data.get('area')
    if not area:
        return Response({'error': 'Area is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    existing_plan = TravelPlan.objects.filter(user=user).first()
    if existing_plan:
        existing_plan.delete()
    
    if area.lower() == 'shibuya':
        quests = Quest.objects.filter(Q(tags__name='Shibuya') | Q(tags__name='Harajuku') | Q(tags__name='Shinjuku') | Q(tags__name='Yoyogi') | Q(tags__name='Ebisu'))
    elif area.lower() == 'asakusa':
        quests = Quest.objects.filter(Q(tags__name='Asakusa') | Q(tags__name='Ueno') | Q(tags__name='Ryogoku') | Q(tags__name='Akihabara'))
    elif area.lower() == 'tokyo':
        quests = Quest.objects.filter(Q(tags__name='Ginza') | Q(tags__name='Akasaka') | Q(tags__name='Azabu') | Q(tags__name='Tokyo') | Q(tags__name='Tsukiji') | Q(tags__name='Kagurazaka'))
    elif area.lower() == 'odaiba':
        quests = Quest.objects.filter(Q(tags__name='Tsukishima') | Q(tags__name='Kasai') | Q(tags__name='Toyosu') | Q(tags__name='Odaiba') | Q(tags__name='Odaba') | Q(tags__name='Roppongi'))

    try:
        morning_quests = random.sample(list(quests.filter(Q(tags__name='Culture') | Q(tags__name='Amusement') | Q(tags__name='Art') | Q(tags__name='Architecture') | Q(tags__name='Local Experience') | Q(tags__name='Shrine') | Q(tags__name='Shopping') | Q(tags__name='Photo Spot') | Q(tags__name='Anime'))), min(2, quests.filter(Q(tags__name='Culture') | Q(tags__name='Amusement') | Q(tags__name='Art') | Q(tags__name='Architecture') | Q(tags__name='Local Experience') | Q(tags__name='Shrine') | Q(tags__name='Shopping') | Q(tags__name='Photo Spot') | Q(tags__name='Anime')).count()))
        lunch_quests = random.sample(list(quests.filter(tags__name='Food')), min(1, quests.filter(tags__name='Food').count()))
        afternoon_quests = random.sample(list(quests.filter(Q(tags__name='Culture') | Q(tags__name='Amusement') | Q(tags__name='Art') | Q(tags__name='Architecture') | Q(tags__name='Local Experience') | Q(tags__name='Shrine') | Q(tags__name='Shopping') | Q(tags__name='Photo Spot') | Q(tags__name='Anime'))), min(3, quests.filter(Q(tags__name='Culture') | Q(tags__name='Amusement') | Q(tags__name='Art') | Q(tags__name='Architecture') | Q(tags__name='Local Experience') | Q(tags__name='Shrine') | Q(tags__name='Shopping') | Q(tags__name='Photo Spot') | Q(tags__name='Anime')).count()))
        break_quests = random.sample(list(quests.filter(Q(tags__name='Sweets') | Q(tags__name='Cafe'))), min(1, quests.filter(Q(tags__name='Sweets') | Q(tags__name='Cafe')).count()))
        evening_quests = random.sample(list(quests.filter(Q(tags__name='Culture') | Q(tags__name='Amusement') | Q(tags__name='Art') | Q(tags__name='Architecture') | Q(tags__name='Local Experience') | Q(tags__name='Shrine') | Q(tags__name='Shopping') | Q(tags__name='Photo Spot') | Q(tags__name='Anime'))), min(2, quests.filter(Q(tags__name='Culture') | Q(tags__name='Amusement') | Q(tags__name='Art') | Q(tags__name='Architecture') | Q(tags__name='Local Experience') | Q(tags__name='Shrine') | Q(tags__name='Shopping') | Q(tags__name='Photo Spot') | Q(tags__name='Anime')).count()))
        dinner_quests = random.sample(list(quests.filter(tags__name='Food')), min(1, quests.filter(tags__name='Food').count()))
        night_quests = random.sample(list(quests.filter(tags__name='Scenery')), min(1, quests.filter(tags__name='Scenery').count()))
        drink_quests = random.sample(list(quests.filter(Q(tags__name='Bar') | Q(tags__name='Izakaya'))), min(1, quests.filter(Q(tags__name='Bar') | Q(tags__name='Izakaya')).count()))
        
        all_quests = morning_quests + lunch_quests + afternoon_quests + break_quests + evening_quests + dinner_quests + night_quests + drink_quests

        travel_plan = TravelPlan.objects.create(user=user)
        travel_plan.quests.set(all_quests)
        travel_plan.save()

        serializer = TravelPlanSerializer(travel_plan)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_travel_plan(request):
    user = request.user
    travel_plan = TravelPlan.objects.filter(user=user).first()
    if travel_plan:
        serializer = TravelPlanSerializer(travel_plan)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'No travel plan found for this user.'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
@transaction.atomic
def save_quest(request, quest_id):
    user = request.user
    quest = get_object_or_404(Quest, id=quest_id)
    
    if SavedQuest.objects.filter(user=user, quest=quest).exists():
        print("Quest already completed")
        return Response({'status': 'quest already completed'}, status=status.HTTP_200_OK)
    
    try:
        save_quest = SavedQuest.objects.create(user=user, quest=quest)
        return Response({'status': 'quest saved'}, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error completing quest: {e}")
        return Response({'status': 'error', 'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_quest_saved(request, quest_id):
    user = request.user
    quest = get_object_or_404(Quest, id=quest_id)
    
    is_saved = SavedQuest.objects.filter(user=user, quest=quest).exists()
    return Response({'is_saved': is_saved}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_quest_completed(request, quest_id):
    user = request.user
    is_completed = QuestCompletion.objects.filter(user=user, quest_id=quest_id).exists()
    return Response({'is_completed': is_completed}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_saved_quests(request):
    user = request.user
    saved_quests = SavedQuest.objects.filter(user=user)
    serializer = SavedQuestSerializer(saved_quests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#一旦不要なやつ
# class TicketViewSet(viewsets.ModelViewSet):
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer
#     permission_classes = [IsAuthenticated]

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @transaction.atomic
# def use_ticket(request, issuance_id):
#     ticket_issuance = get_object_or_404(TicketIssuance, id=issuance_id)
    
#     # 既に使用されているかをチェック
#     if ticket_issuance.used:
#         logger.info("Ticket already used")
#         return Response({'status': 'ticket already used'}, status=status.HTTP_200_OK)
    
#     # チケット使用処理
#     try:
#         ticket_issuance.used = True
#         ticket_issuance.save()
#         logger.info("Ticket used successfully")
#         return Response({'status': 'ticket used'}, status=status.HTTP_200_OK)
#     except Exception as e:
#         logger.error(f"Error using ticket: {e}")
#         return Response({'status': 'error', 'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @transaction.atomic
# def claim_ticket(request, ticket_id):
#     user = request.user
#     ticket = get_object_or_404(Ticket, id=ticket_id)
    
#     # 既にチケットが請求されているかをチェック
#     if TicketIssuance.objects.filter(user=user, ticket=ticket).exists():
#         logger.info("Ticket already claimed")
#         return Response({'status': 'ticket already claimed'}, status=status.HTTP_200_OK)
    
#     # チケット請求処理
#     try:
#         ticket_issuance = TicketIssuance.objects.create(user=request.user, ticket=ticket)
#         ticket.issued_to.add(user)
#         ticket.save()
#         logger.info("Ticket claimed successfully")
#         return Response({'status': 'ticket claimed'}, status=status.HTTP_200_OK)
#     except Exception as e:
#         logger.error(f"Error claiming ticket: {e}")
#         return Response({'status': 'error', 'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_ticket_issuances(request, ticket_id):
#     ticket = get_object_or_404(Ticket, id=ticket_id)
#     issuances = TicketIssuance.objects.filter(ticket=ticket)
#     serializer = TicketIssuanceSerializer(issuances, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_reports(request):
#     user = request.user
#     reports = Report.objects.filter(user=user)
#     serializer = ReportSerializer(reports, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def generate_report(request):
#     user = request.user
#     report_content = generate_report_content(user)
#     if report_content is None:
#         return Response({'status': 'Report already exists'}, status=status.HTTP_200_OK)
#     user.done = True
#     user.save()
#     report = Report.objects.create(user=user, content=report_content)
#     serializer = ReportSerializer(report)
#     return Response(serializer.data, status=status.HTTP_201_CREATED)

# def start():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(handle, 'interval', days=1)  # 1日に1回ジョブを実行するようにスケジュール
#     scheduler.start()

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def report_view(request):
#     request_id = uuid.uuid4()
#     print(f"Request {request_id} - Report View accessed")  # デバッグ情報
#     print(f"Request {request_id} - User {request.user.id} done flag: {request.user.done}")  # ユーザーのdoneフラグをログに出力
#     try:
#         if request.user.done:
#             print(f"Request {request_id} - User {request.user.id} has done flag set to True")  # デバッグ情報
#             report = Report.objects.get(user=request.user)
#             serializer = ReportSerializer(report)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             print(f"Request {request_id} - User {request.user.id} does not have permission")  # デバッグ情報
#             return Response({'detail': 'You do not have permission to view this resource.'}, status=status.HTTP_403_FORBIDDEN)
#     except Report.DoesNotExist:
#         print(f"Request {request_id} - Report not found for user {request.user.id}")  # デバッグ情報
#         return Response({'detail': 'Report not found.'}, status=status.HTTP_404_NOT_FOUND)

# def handle():
#     now = timezone.now()
#     users = User.objects.filter(due__lt=now, done=False)

#     for user in users:
#         user.done = True
#         user.save()

#         report_content = generate_report_content(user)
#         Report.objects.create(user=user, content=report_content)

# def generate_report_content(user):
#     if Report.objects.filter(user=user).exists():
#         return None  # 既にレポートが存在する場合、新しいレポートを生成しない

#     completed_quests = QuestCompletion.objects.filter(user=user)
#     report_content = f'Report for {user.first_name} {user.last_name}:\n\n'
#     report_content += f'Completed Quests:\n'
#     for completion in completed_quests:
#         report_content += f'- {completion.quest.title} (Completed on {completion.completion_date})\n'
#     return report_content