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
        if self.action == "create":
            return CreateUserSerializer
        if self.action == "subscribe":
            return FollowSerializer
        return CustomUserSerializer

    @action(detail=False, methods=["GET"],
            permission_classes=[IsAuthenticated], )
    def me(self, request):
        serializer = CustomUserSerializer(request.user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, permission_classes=[IsAuthenticated], )
    def subscriptions(self, request):
        queryset = Follow.objects.filter(user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages, many=True,)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=["POST", "DELETE"],
            permission_classes=[IsAuthenticated], )
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, pk=id)
        if request.method == "POST":
            serializer = FollowSerializer(
                Follow.objects.create(user=request.user, author=author),
                context={"request": request}, )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == "DELETE":
            Follow.objects.filter(
                user=request.user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
