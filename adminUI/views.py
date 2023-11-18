from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .serializers import CustomUserSerializer
from .models import CustomUser


class UserRegistrationView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    # not used in the create method, but it's a required attribute for CreateAPIView
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        # Check if a user with the provided username or email already exists
        username = request.data.get('username', None)
        email = request.data.get('email', None)

        if username and get_user_model().objects.filter(username=username).exists():
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        if email and get_user_model().objects.filter(email=email).exists():
            return Response({'error': 'Email address already registered.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # creating an instance of your serializer (CustomUserSerializer) with the data from the request.

        self.perform_create(serializer)
        # calls the save method on the serializer

        headers = self.get_success_headers(serializer.data)
        # This line is getting the success headers for the response.

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        print(request.data['username'])
        print(request.data['password'])
        if response.status_code == status.HTTP_200_OK:
            user = CustomUser.objects.filter(username=request.data['username']).first()

            if user:
                token, created = Token.objects.get_or_create(user=user)
                response.data['token'] = token.key
            else:
                # Handle the case where the user is not found
                response.data['non_field_errors'] = ['User not found.']
        return response

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # Retrieve the current user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        # This is a flag that indicates whether to perform a partial update. It's set based on the presence of the partial parameter in the request.
        instance = self.get_object()
        # Retrieves the current user (object to be deleted) using the get_object method.
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
