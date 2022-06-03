from cgitb import handler
from django.shortcuts import render
from django.http.response import JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes

from account.models import Account
from advertisement.models import Advertisement
from advertisement.api.serializers import AddAdvertisementSerializer, ShowAdvertisementSerializer

from os.path import realpath,dirname,join
import sys
project_path = dirname(dirname(dirname(dirname(realpath(__file__)))))
sys.path += [join(project_path,'WebScrapper/')]
from scraper import handler


@csrf_exempt
@api_view(["POST", ])
@permission_classes([IsAuthenticated])
def add_ad_view(request):
    try:
        ad_data = JSONParser().parse(request)
        ad_data["seller"] = request.user.id

        ad_serializer = AddAdvertisementSerializer(data=ad_data)
        if ad_serializer.is_valid():
            ad = ad_serializer.save()

            return JsonResponse({ 'v': True, 'm': ad.id }, safe=False)

        return JsonResponse({ 'v': False, 'm': ad_serializer.errors }, safe=False)
    except IntegrityError as e:
        return JsonResponse({ 'v': False, 'm': str(e) }, safe=False)
    except KeyError as e:
        return JsonResponse({ 'v': False, 'm': str(e) }, safe=False)

@csrf_exempt
@api_view(["POST", ])
@permission_classes([IsAuthenticated])
def update_ad_img_view(request, id):
    try:
        ad = Advertisement.objects.get(id=id)
    except BaseException as e:
        return JsonResponse({ 'v': False, 'm': ValidationError(str(e)) }, safe=False)
    
    file = request.FILES['img']
    extension = file.name.split('.')[-1]
    file_name = "exercises/" + str(id) + "." + extension

    if default_storage.exists(file_name):
        default_storage.delete(file_name)

    file_path = default_storage.save(file_name, file)
    ad.img = file_path

    ad.save()
    return JsonResponse({ 'v': True, 'm': None}, safe=False)

@csrf_exempt
@api_view(["GET", ])
@permission_classes([IsAuthenticated])
def get_all_ads_view(request):
    try:
        data = JSONParser().parse(request)
        ads_list = []
        for ad in Advertisement.objects.all():
            ad_data = ShowAdvertisementSerializer(ad).data
            ad_data['marketplace'] = "Bom e Barato"
            ad_data['link']= None
            ads_list.append(ad_data)
        if 'marketplaces' in data:
            ads_list += handler(data['search_term'], data['max_pages'], data['marketplaces'])
        else:
            ads_list +=handler(data['search_term'], data['max_pages'])
        
        return JsonResponse(ads_list, safe=False)
    except BaseException as e:
        return JsonResponse({ 'v': False, 'm': str(e) }, safe=False)

@csrf_exempt
@api_view(["GET", ])
@permission_classes([IsAuthenticated])
def get_promoted_ads_view(request):
    try:
        ads_list=[]
        for ad in Advertisement.objects.all():
            ad_data = ShowAdvertisementSerializer(ad).data
            ad_data['marketplace'] = "Bom e Barato"
            ad_data['link']= None
            ads_list.append(ad_data)
        return JsonResponse(ads_list, safe=False)
    except BaseException as e:
        return JsonResponse({ 'v': False, 'm': str(e) }, safe=False)