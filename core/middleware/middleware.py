from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from urllib.parse import unquote

class DemoModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if '/delete/' in request.path.lower():
            html = """
            <html>
            <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        text-align: center;
                        background-color: #f4f4f4;
                        color: #333;
                        padding: 50px 0;
                    }
                    .error-container {
                        background-color: #fff;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 0 15px rgba(0,0,0,0.1);
                        max-width: 500px;
                        margin: auto;
                    }
                </style>
            </head>
            <body>
                <div class="error-container">
                    <h2>Deletions are not allowed in demo mode.</h2>
                </div>
            </body>
            </html>
            """
            return HttpResponseForbidden(html)
        
        response = self.get_response(request)
        return response


class SlugDecodeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.path_info = unquote(request.path_info)
        response = self.get_response(request)
        return response
