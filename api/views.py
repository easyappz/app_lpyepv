from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count

from api.models import Member, Message
from api.serializers import (
    MemberSerializer,
    MemberRegistrationSerializer,
    MemberLoginSerializer,
    MessageSerializer,
)
from api.authentication import TokenAuthentication, generate_token


class RegisterView(APIView):
    """Register a new member and return access token"""
    
    def post(self, request):
        serializer = MemberRegistrationSerializer(data=request.data)
        
        if not serializer.is_valid():
            error_response = {
                "error": "Ошибка валидации",
                "field_errors": serializer.errors
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        
        # Create member
        member = serializer.save()
        
        # Generate token
        token = generate_token()
        member.auth_token = token
        member.save()
        
        # Return token response
        response_data = {
            "access_token": token,
            "token_type": "Bearer",
            "username": member.username,
            "user_id": member.id
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """Login member and return access token"""
    
    def post(self, request):
        serializer = MemberLoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            error_response = {
                "error": "Ошибка валидации",
                "field_errors": serializer.errors
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        
        # Get validated member
        member = serializer.validated_data['member']
        
        # Generate new token
        token = generate_token()
        member.auth_token = token
        member.save()
        
        # Return token response
        response_data = {
            "access_token": token,
            "token_type": "Bearer",
            "username": member.username,
            "user_id": member.id
        }
        
        return Response(response_data, status=status.HTTP_200_OK)


class ProfileView(APIView):
    """Get current member profile"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = MemberSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessageListView(APIView):
    """Get list of all messages with pagination"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get pagination parameters
        limit = int(request.query_params.get('limit', 50))
        offset = int(request.query_params.get('offset', 0))
        
        # Validate pagination parameters
        if limit < 1 or limit > 100:
            limit = 50
        if offset < 0:
            offset = 0
        
        # Get total count
        total = Message.objects.count()
        
        # Get paginated messages
        messages = Message.objects.select_related('member').all()[offset:offset+limit]
        
        # Serialize messages
        serializer = MessageSerializer(messages, many=True)
        
        response_data = {
            "messages": serializer.data,
            "total": total
        }
        
        return Response(response_data, status=status.HTTP_200_OK)


class MessageCreateView(APIView):
    """Create a new message from authenticated member"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Validate text field
        text = request.data.get('text', '').strip()
        
        if not text:
            error_response = {
                "error": "Ошибка валидации",
                "field_errors": {
                    "text": ["Текст сообщения не может быть пустым"]
                }
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        
        if len(text) > 1000:
            error_response = {
                "error": "Ошибка валидации",
                "field_errors": {
                    "text": ["Текст сообщения не может превышать 1000 символов"]
                }
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        
        # Create message
        message = Message.objects.create(
            member=request.user,
            text=text
        )
        
        # Serialize and return
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
