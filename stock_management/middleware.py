import json

import requests
from django.http import JsonResponse


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def process_view(self, request, view_func, view_args, view_kwargs):
        authentication_token = request.headers.get("Authentication")
        if authentication_token:
            url = f"http://127.0.0.1:5001/v1/validateToken"

            payload = {}
            headers = {"Authorization": f"Bearer {authentication_token}"}
            try:
                response = requests.request("POST", url, headers=headers, data=payload)

                user_info = json.loads(response.text)
                user = user_info["user_info"].get("user_type")
                if user.lower() == "buyer":
                    return JsonResponse(
                        dict(
                            errorMessage=f"'buyer' cannot access this endpoint",
                            errorCode="Entity Not Allowed",
                        ),
                        status=403,
                    )
                return None
            except Exception as error:
                return JsonResponse(
                    dict(
                        errorMessage=f"{str(error)}",
                        errorCode="Authentication Microservice Error",
                    ),
                    status=500,
                )

        return JsonResponse(
            dict(
                errorMessage="Provide 'Authentication' in headers",
                errorCode="Authentication Error",
            ),
            status=401,
        )


    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
