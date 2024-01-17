from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
import json


def read_from_database():
    """
    Reads from db.json and returns a dictionary of the data.

    Creates db.json if it does not exist.
    """

    # Load JSON database.
    try:
        with open('db.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        # JSON database does not exist, create it.
        data = {}
        with open('db.json', 'w') as f:
            json.dump(data, f)

    return data


@csrf_exempt
def registration_handler(request):
    """
    Handles user registration requests.
    """

    # Retrieve username and password from POST data.
    username = request.POST.get('username')
    password = request.POST.get('password')

    # If no username and password is provided, return an error.
    if not username or not password:
        return JsonResponse({"status": "error", "message": "Username and password not provided"})
    
    # Create user. If user already exists, return an error.
    try:
        User.objects.create_user(username=username, password=password)
    except IntegrityError:
        return JsonResponse({"status": "error", "message": "User already exists"})

    # Return success message.
    return JsonResponse({"status": "success"})


@csrf_exempt
def data_handler(request):
    """
    Handle requests to upload and retrieve user data from the database.

    User authentication is required for both GET and POST requests.
    GET requests retrieve data from the database.
    POST requests upload data to the database.
    """

    if request.method == 'GET':
        # Retrieve username and password from GET query parameters.
        username = request.GET.get('username')
        password = request.GET.get('password')

        # If no username and password is provided, return an error.
        if not username or not password:
            return JsonResponse({"status": "error", "message": "Username and password not provided"})

        # Authenticate user.
        user = authenticate(request, username=username, password=password)

        # If user is authenticated, proceed.
        if user is not None:
            # Load JSON database.
            json_data = read_from_database()

            # Retrieve and return user data from JSON database.
            user_data = json_data.get(username, {})
            return JsonResponse(user_data)
        else:
            # If user is not authenticated, return an error.
            return JsonResponse({"status": "error", "message": "Invalid credentials"})

    elif request.method == 'POST':
        # Retrieve username and password from POST data.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Retrieve and decode JSON data from POST data.
        received_data = json.loads(request.POST.get('json'))

        # If no username and password is provided, return an error.
        if not username or not password:
            return JsonResponse({"status": "error", "message": "Username and password not provided"})

        # Authenticate user.
        user = authenticate(request, username=username, password=password)

        # If user is authenticated, proceed.
        if user is not None:
            # Load JSON database.
            json_data = read_from_database()

            # Add user data to JSON database.
            json_data[username] = received_data

            # Save JSON database.
            with open('db.json', 'w') as f:
                json.dump(json_data, f)

            # Return success message.
            return JsonResponse({"status": "success"})
        else:
            # If user is not authenticated, return an error.
            return JsonResponse({"status": "error", "message": "Invalid credentials"})



@csrf_exempt
def delete_user_handler(request):
    """
    Handles requests to delete user data from the database.

    User authentication is required.
    """

    # Retrieve username and password from POST data.
    username = request.POST.get('username')
    password = request.POST.get('password')

    # If no username and password is provided, return an error.
    if not username or not password:
        return JsonResponse({"status": "error", "message": "Username and password not provided"})

    # Authenticate user.
    user = authenticate(request, username=username, password=password)

    # If user is authenticated, proceed.
    if user is not None:
        # Load JSON database.
        json_data = read_from_database()

        # Delete user data from JSON database.
        json_data.pop(username, None)

        # Save JSON database.
        with open('db.json', 'w') as f:
            json.dump(json_data, f)

        # Return success message.
        return JsonResponse({"status": "success"})
    else:
        # If user is not authenticated, return an error.
        return JsonResponse({"status": "error", "message": "Invalid credentials"})

