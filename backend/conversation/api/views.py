from django.http.response import JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from conversation.models import Conversation

from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes

from conversation.api.serializers import AddConversationSerializer
from django.db.models import Q

@csrf_exempt
@api_view(["POST", ])
@permission_classes([IsAuthenticated])
def add_message_view(request):
    try:
        message_data = JSONParser().parse(request)
        message_data["sender"] = request.user.id 

        msg_serializer = AddConversationSerializer(data=message_data)
        if msg_serializer.is_valid():
            msg_serializer.save()

            return JsonResponse({ 'v': True, 'm': None }, safe=False)

        return JsonResponse({ 'v': False, 'm': msg_serializer.errors }, safe=False)
    except IntegrityError as e:
        return JsonResponse({ 'v': False, 'm': str(e) }, safe=False)
    except KeyError as e:
        return JsonResponse({ 'v': False, 'm': str(e) }, safe=False)
    except BaseException as e:
        return JsonResponse({ 'v': False, 'm': str(e) }, safe=False)

@csrf_exempt
@api_view(["GET", ])
@permission_classes([IsAuthenticated])
def get_conversation_view(request, id):
    try:
        message_list = []
        for message in Conversation.objects.filter(receiver=request.user.id, sender=id).order_by('timestamp'):
            if message.sender == request.user.id:
                message_list.append( 'sender' + ':' + message.message )
            elif message.receiver == request.user.id:
                message_list.append( 'receiver' + ':' + message.message )

        if not message_list:
            return JsonResponse({ 'v': True, 'm': 'No messages' }, safe=False)
        
        return JsonResponse(message_list, safe=False)
    except IntegrityError as e:
        return JsonResponse({ 'v': False, 'm': str(e) }, safe=False)
    except KeyError as e:
        return JsonResponse({ 'v': False, 'm': str(e) }, safe=False)
    except BaseException as e:
        return JsonResponse({ 'v': False, 'm': str(e) }, safe=False)

@csrf_exempt
@api_view(["GET", ])
@permission_classes([IsAuthenticated])
def get_my_conversations_view(request):
    try:
        chats_overview=[]
        for msg in Conversation.objects.filter(Q(receiver=request.user.id) | Q(sender=request.user.id)).order_by('-timestamp'):
            pass
        return JsonResponse(chats_overview, safe=False)
    except BaseException as e:
        return JsonResponse({ 'v': False, 'm': str(e) }, safe=False)