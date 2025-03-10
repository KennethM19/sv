import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({"error": "Email and password are required"}, status=400)

    try:
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={settings.FIREBASE_WEB_API_KEY}"
        response = requests.post(url, json={"email": email, "password": password, "returnSecureToken": True})
        response_data = response.json()

        if "idToken" in response_data:
            return Response(
                {"message": "Login Successful", "token": response_data["idToken"], "uid": response_data["localId"]})
        else:
            return Response({"error": response_data.get("error", {}).get("message", "Login error")}, status=400)

    except Exception as e:
        return Response({"error": str(e)}, status=400)