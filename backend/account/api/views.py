from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.db import IntegrityError
from django.contrib.auth import login, logout

from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from .tokens import account_deactivation_token
from django.contrib.auth.models import User  
from django.core.mail import EmailMultiAlternatives

from account.api.serializers import RegistrationSerializer
from account.models import Account
from account.api.utils import *
from django.core.files.storage import default_storage
from django.core.validators import validate_email


# Everyone can acess this view
# Receives JSON with keyswords "email", "first_name", "last_name", "birth_date", "password", "role" that can't be null
# Keyword "role" can only be 1(Student) or 2(Teacher)
# If sucessfull registration returns { "v": True, "m": None }
# If unsuccessful registration:
# Email already in use returns { "v": False, "m": "account with this email already exists" }
# Email not valid returns { "v": False, "m": "Enter a valid email address" }
# ATTENTION: Both cases above can happen at the same time
@csrf_exempt
@api_view(["POST",])
@permission_classes([AllowAny])
def registration_view(request):
    try:
        data = {}
        account_serializer = RegistrationSerializer(data=JSONParser().parse(request))  # Handles received data and instanciated user
        if account_serializer.is_valid():                                               # Checks if serializer is valid
            account = account_serializer.save()                                         # Saves new user
            account.is_active = True
            account.save()

            return JsonResponse({ 'v': True, 'm': None}, safe=False)

        return JsonResponse({ 'v': False, 'm': account_serializer.errors }, safe=False)

    except IntegrityError as e:
            account = Account.objects.get(username='')
            account.delete()
            data['v'] = False
            data['m'] = ValidationError(str(e))
            return JsonResponse(data, safe=False)
    except KeyError as e:
            data['v'] = False
            data['m'] = ValidationError(str(e))
            return JsonResponse(data, safe=False)

# Everyone can acess this view
# Receives JSON with keyswords "email", "password" that can't be null
# If sucessfull login returns: { "v":True, "m": None, "token": generated_auth_token }
# If account not found returns: { "v":False, "m": "Account not found" }
# If unsuccessful login returns: "Incorrect Credentials" 
# If account is inactive returns: "Account not active"
@csrf_exempt
@api_view(["POST",])
@permission_classes([AllowAny])
def login_view(request):
    login_data = JSONParser().parse(request)                                            # Handles received data
    try:
        account = Account.objects.get(email=login_data['email'])                        # Gets account of user with the given email
    except BaseException as e:
        return JsonResponse({ 'v': False, 'm': "Account not found" }, safe=False)

    if not account.check_password(login_data["password"]):                              # Checks if the given password is correct
        return JsonResponse({ 'v': False, 'm': "Incorrect Credentials" }, safe=False)

    if account:
        data = {}
        if account.is_active:
            login(request, account)                                                     # Logs in user
            data['v'] = True
            data['m'] = None
            data['t'] = Token.objects.get_or_create(user=account)[0].key                # Creates or gets token for that specific user
            data['id'] = account.id
            return JsonResponse(data, safe=False)
        else:
            data['v'] = False
            data['m'] = "Not active"
            return JsonResponse(data, safe=False) 
    else:
        return JsonResponse({ 'v': False, 'm': 'Account not found' }, safe=False)

# Only authenticated users can acess this view aka in HTTP header add "Authorization": "Bearer " + generated_auth_token
# Takes user's auth token, deletes it and logouts out user
# If sucessfull returns { "v":True, "m": None }
# If failed returns { "v":False, "m": Error message }
@csrf_exempt
@api_view(["POST", ])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        request.user.auth_token.delete()        # Deletes user's auth_token
        logout(request)                         # Logs out user

        return JsonResponse({ 'v': True, 'm': None }, safe=False)
    except Exception as e:
        return JsonResponse({ 'v': False, 'm': str(e) }, safe=False)

# Only authenticated users can acess this view aka in HTTP header add "Authorization": "Bearer " + generated_auth_token
# Receives JSON with keyswords "old_pwd", "new_pwd" that can't be null
# If sucessfull it changes user password and returns: { "v": True, "m": None, "token": generated_auth_token }
# If unsuccessful nothing happens and returns: { "v": False, "m": Error message } 
@csrf_exempt
@api_view(["POST", ])
@permission_classes([IsAuthenticated])
def change_password(request):
    packet = JSONParser().parse(request)                    # Handles received data
    try:
        account = Account.objects.get(email=request.user)   # Gets account of user that sent the request (trough generated_auth_token)
    except BaseException as e:
        return JsonResponse({ 'v': False, 'm': ValidationError(str(e)) }, safe=False)
    
    if not account.check_password(packet['old_pwd']):       # Checks if the current password is correct
        return JsonResponse({ 'v': False, 'm': "Incorrect Credentials" }, safe=False)

    if account.is_active:
        account.set_password(packet['new_pwd'])     # Sets new password as current password
        account.save()                              # Saves changes
        login(request, account)                     # Logs user again
        data = {}
        data['v'] = True
        data['m'] = None
        data['t'] = Token.objects.get_or_create(user=account)[0].key    # Creates or gets token for that specific user
        
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({ 'v': False, 'm': "Not Active" }, safe=False)

# Only authenticated users can acess this view aka in HTTP header add "Authorization": "Bearer " + generated_auth_token
# Receives user token and gets user info
# If sucessfull returns: { "v": True, "m": None, "info": {"first_name", "last_name", "email", "birth_date", "joined", "role" }}
# If unsuccessful returns: { "v": False, "m": Error message } 
@csrf_exempt
@api_view(["GET",])
@permission_classes([IsAuthenticated])
def profile_view(request):
    try:
        account = Account.objects.get(email=request.user)   # Gets account of user that sent the request (trough generated_auth_token)
    except BaseException as e:
        return JsonResponse({ 'v': False, 'm': ValidationError(str(e)) }, safe=False)

    info = {}
    info['first_name'] = account.first_name
    info['last_name'] = account.last_name
    info['email'] = account.email
    info['birth_date'] = account.birth_date
    info['joined'] = account.date_joined
    info['id'] = account.id

    try:
        info['avatar'] = account.avatar.url
    except BaseException as e:
        info['avatar'] = None

    return JsonResponse({ 'v': True, 'm': None, 'info': info }, safe=False)

# Only authenticated users can acess this view aka in HTTP header add "Authorization": "Bearer " + generated_auth_token
# Receives JSON with keyswords "password", "email" that can't be null
# If sucessfull makes the user inactive and returns: { "v": True, "m": None }
# If unsuccessful returns: { "v": False, "m": Error message } 
@csrf_exempt
@api_view(["POST",])
@permission_classes([IsAuthenticated])   
def delete_view(request, token):
    packet = JSONParser().parse(request)                    # Handles received data
    try:
        account = Account.objects.get(email=request.user)   # Gets account of user that sent the request (trough generated_auth_token)
    except BaseException as e:
        return JsonResponse({ 'v': False, 'm': ValidationError(str(e)) }, safe=False)

    if not account.check_password(packet['password']) or account.email != packet['email']:       # Checks if the current password is correct
        return JsonResponse({ 'v': False, 'm': "Incorrect Credentials" }, safe=False)

    if account is not None and account_deactivation_token.check_token(account, token):  
        account.is_active = False
        account.email = str(account.id) + "@deleted.com"
        account.first_name = ""
        account.last_name = ""
        account.role = 0
        account.save()

        return JsonResponse({ 'v': True, 'm': None}, safe=False)

    return JsonResponse({ 'v': True, 'm':"Something went wrong"}, safe=False)


# Only authenticated users can acess this view aka in HTTP header add "Authorization": "Bearer " + generated_auth_token
# Receives JSON with keyswords "email", "first_name", "last_name", "birth_date" that can't be null
# If sucessfull updates user data and returns: { "v": True, "m": None }
# If unsuccessful returns: { "v": False, "m": Error message } 
@csrf_exempt
@api_view(["PATCH",])
@permission_classes([IsAuthenticated]) 
def update_profile(request):
    packet = JSONParser().parse(request)                    # Handles received data
    
    try:
        account = Account.objects.get(email=request.user)   # Gets account of user that sent the request (trough generated_auth_token)
        account_serialzier = RegistrationSerializer(instance=account, data=packet, partial=True)
        if account_serialzier.is_valid():
         
            account_serialzier.update(account, account_serialzier.validated_data)
            return JsonResponse({ 'v': True, 'm': None}, safe=False)

        return JsonResponse({ 'v': False, 'm': account_serialzier.errors }, safe=False)
    except IntegrityError as e:
        return JsonResponse({ 'v': False, 'm': str(e) }, safe=False)
    except KeyError as e:
        return JsonResponse({ 'v': False, 'm': str(e) }, safe=False)
    except BaseException as e:
        return JsonResponse({ 'v': False, 'm': str(e) }, safe=False)

# Only authenticated users can acess this view aka in HTTP header add "Authorization": "Bearer " + generated_auth_token
# Receives a form-data with key "avatar" that can't be null
# If sucessfull updates user data and returns: { "v": True, "m": None }
# If unsuccessful returns: { "v": False, "m": Error message } 
@csrf_exempt
@api_view(["POST",])
@permission_classes([IsAuthenticated]) 
def upload_avatar(request):
    try:
        account = Account.objects.get(email=request.user)   # Gets account of user that sent the request (trough generated_auth_token)
    except BaseException as e:
        return JsonResponse({ 'v': False, 'm': ValidationError(str(e)) }, safe=False)

    file = request.FILES['avatar']
    extension = file.name.split('.')[-1]
    file_name = "users/" + str(account.id) + "." + extension

    if default_storage.exists(file_name):
        default_storage.delete(file_name)

    file_path = default_storage.save(file_name, file)
    account.avatar = file_path

    account.save()
    return JsonResponse({ 'v': True, 'm': None}, safe=False)
