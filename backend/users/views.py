from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.paginators import PageLimitPagination
from api.serializers import (CreateUserSerializer, CustomUserSerializer,
                             FollowSerializer)
from users.models import Follow, User


class CustomUserViewSet(UserViewSet):
    """Вьюсет для модели пользователя."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = PageLimitPagination
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        method = self.request.method
        if method in ["POST", "PUT", "PATCH"]:
            return CreateUserSerializer
        return CustomUserSerializer

    @action(detail=False, methods=["GET"],
            permission_classes=[IsAuthenticated], )
    def me(self, request):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        follows = self.paginate_queryset(
            User.objects.filter(following__user=request.user))
        serializer = FollowSerializer(
            follows, many=True,
            context={"request": request})
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=["POST", "DELETE"],
            permission_classes=[IsAuthenticated], )
    def subscribe(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.user)
        author = get_object_or_404(User, id=self.kwargs.get('id'))
        follow_queryset = Follow.objects.filter(
            author=author, user=user)
        follow_exists = follow_queryset.exists()
        if request.method == "POST":
            if follow_exists:
                return Response(
                    {"errors": "Нельзя 2 раза подписаться на одного автора!"},
                    status=status.HTTP_400_BAD_REQUEST)
            if user == author:
                return Response(
                    {"errors": "Нельзя подписаться на самого себя!"},
                    status=status.HTTP_400_BAD_REQUEST)
            serializer = FollowSerializer(
                author, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == "DELETE":
            follow_queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
