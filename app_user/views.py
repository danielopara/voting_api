from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import  AppUser
from .serializers import AppUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view


# Create your views here.
class UserView():
    @api_view(['POST'])
    def register(request):
        serializer = AppUserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    @api_view((['GET']))
    def get_users(request):
        users = AppUser.objects.all()
        
        user_list = [
            {
                "id": user.usr_id,
                'full_name': user.full_name,
                'email': user.user.email
            }
            for user in users
        ]
        user = AppUserSerializer(users, many=True)
        return Response({'success': True, 'data': user_list}, status=status.HTTP_200_OK)
    
    @api_view(['GET'])
    def get_user_by_id(request,usr_id):
        try:
            user = AppUser.objects.get(usr_id=usr_id)
        except AppUser.DoesNotExist:
            return Response({'status':False,'message': "user does not exist"}, status=status.HTTP_404_NOT_FOUND)

        main_user =AppUserSerializer(user)
        return Response({'status': True, 'data': main_user.data}, status=status.HTTP_200_OK)