from codinghobbies.api.mixins import ApiAuthMixin
from codinghobbies.api.pagination import LimitOffsetPagination, get_paginated_response
from codinghobbies.blog.models import Subscription
from codinghobbies.blog.selectors.post import get_subscribers
from codinghobbies.blog.services.post import subscribe, unsubscribe

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from drf_spectacular.utils import extend_schema


class SubscribeDetailApi(ApiAuthMixin, APIView):

    def delete(self, request, email):
        try:
            unsubscribe(user=request.user, email=email)
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
        

class SubscribeApi(ApiAuthMixin, APIView):

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class InputSubSerializer(serializers.Serializer):
        email = serializers.CharField(max_length=100)
    
    class OutPutSerializer(serializers.ModelSerializer):
        email = serializers.SerializerMethodField("get_username")

        class Meta:
            model = Subscription
            fields = ("email",)

        def get_username(self, subscription):
            return subscription.target.email
        

    @extend_schema(responses=OutPutSerializer)
    def get(self, request):
        user = request.user
        query = get_subscribers(user=user)
        return get_paginated_response(
            request=request,
            pagination_class=self.Pagination,
            queryset=query,
            serializer_class=self.OutPutSerializer,
            view=self
            )

    @extend_schema(
        request=InputSubSerializer,
        responses=OutPutSerializer
    )
    def post(self, request):
        serializer = self.InputSubSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            query = subscribe(user=request.user, email=serializer.validated_data.get("email"))
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST
            ) 
        return Response(self.OutPutSerializer(query, context={"request":request}).data)
