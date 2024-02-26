from django.shortcuts import render
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from .serializers import User_Sign_Up
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.template.loader import render_to_string
from rest_framework.response import Response
# Create your views here.


class Signup(APIView):
    template_name = "account_activation.html"
    def post(self, request):
        serializer = User_Sign_Up(data=request.data)
        data = request.data
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(
                user
            )  # Create a verification token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_url = reverse(
                "verify-user", kwargs={"uidb64": uid, "token": token}
            )  # Construct the verification URL
            context = {
                "user": user,
                "verification_url": request.build_absolute_uri(
                    verification_url
                ),  # Render the HTML content of the email
            }
            email_html_message = render_to_string(
                "account_activation.html", context
            )
            # Send the verification email
            subject = "TITLIS | Activate Your Account"
            from_email = "cootinternational@gmail.com"
            recipient_list = [user.email]

            send_mail(
                subject,
                email_html_message,
                from_email,
                recipient_list,
                html_message=email_html_message,
                fail_silently=True,
            )


            data = {"Text": "registered", "status": 201}
            return Response(data=data)
        else:
            statusText = serializer.errors
            data = {"Text": statusText, "status": 404}
            return Response(data=data)

