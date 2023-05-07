from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, FriendshipRequest, Friendship
from .serializers import UserSerializer, FriendshipRequestSerializer, FriendshipSerializer


@api_view(['POST', 'GET'])
def users(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['GET', 'POST', 'DELETE'])
def friend_status(request, user_id, friend_id):
    user = get_object_or_404(User, pk=user_id)
    friend = get_object_or_404(User, pk=friend_id)

    if user == friend:
        return Response({'status': 'тот же пользователь'}, status=status.HTTP_400_BAD_REQUEST)

    friendship = Friendship.objects.filter(user1=min(user, friend), user2=max(user, friend))
    fr_out = FriendshipRequest.objects.filter(from_user=user, to_user=friend)
    fr_in = FriendshipRequest.objects.filter(from_user=friend, to_user=user)

    if request.method == 'GET':
        if friendship.exists():
            return Response({'status': 'уже друзья'})
        if fr_out.exists():
            return Response({'status': 'есть исходящая заявка'})
        if fr_in.exists():
            return Response({'status': 'есть входящая заявка'})
        return Response({'status': 'ничего нет'})

    elif request.method == 'POST':
        if fr_in.exists():
            # Создание дружбы
            friendship = Friendship(user1=min(user, friend), user2=max(user, friend))
            friendship.save()
            fr_in.delete()
            return Response(FriendshipSerializer(friendship).data, status=status.HTTP_201_CREATED)
        if friendship.exists():
            return Response({'status': 'уже друзья'}, status=status.HTTP_423_LOCKED)
        if fr_out.exists():
            return Response({'status': 'уже есть исходящая заявка'}, status=status.HTTP_423_LOCKED)
        fr_in = FriendshipRequest(from_user=user, to_user=friend)
        fr_in.save()
        return Response(FriendshipRequestSerializer(fr_in).data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        if friendship.exists():
            fr_in = FriendshipRequest(from_user=friend, to_user=user)
            fr_in.save()
            friendship.delete()
        elif fr_out.exists():
            fr_out.delete()
        return Response()


@api_view(['POST'])
def accept_friend_request(request, user_id, friend_id):
    user = get_object_or_404(User, pk=user_id)
    friend = get_object_or_404(User, pk=friend_id)
    friend_request = get_object_or_404(FriendshipRequest, from_user=friend, to_user=user)
    friendship = Friendship(user1=min(user, friend), user2=max(user, friend))
    friendship.save()
    friend_request.delete()
    return Response(FriendshipSerializer(friendship).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def reject_friend_request(request, user_id, friend_id):
    user = get_object_or_404(User, pk=user_id)
    friend = get_object_or_404(User, pk=friend_id)
    friend_request = get_object_or_404(FriendshipRequest, from_user=friend, to_user=user)
    friend_request.delete()
    return Response()


@api_view(['GET'])
def get_friends_sent(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    friend_requests_sent = FriendshipRequest.objects.filter(from_user=user)
    serializer_sent = FriendshipRequestSerializer(friend_requests_sent, many=True)
    return Response(serializer_sent.data)


@api_view(['GET'])
def get_friends_receive(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    friend_requests_receive = FriendshipRequest.objects.filter(to_user=user)
    serializer_receive = FriendshipRequestSerializer(friend_requests_receive, many=True)
    return Response(serializer_receive.data)


@api_view(['GET'])
def get_friends(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    friendships = Friendship.objects.filter(user1=user) | Friendship.objects.filter(user2=user)
    friends = []
    for friendship in friendships:
        friend = friendship.user1 if friendship.user2 == user else friendship.user2
        friends.append(friend)
    serializer = UserSerializer(friends, many=True)
    return Response(serializer.data)
