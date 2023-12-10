from django.shortcuts import render

import logging

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.renderers import JSONRenderer
import json
from django.http import JsonResponse
from .serializers import MpesaCheckoutSerializer
from .util import MpesaGateWay
from.callback_handler import callback_handler
from .models import Transaction
from .serializers import TransactionSerializer

gateway = MpesaGateWay()

@authentication_classes([])
@permission_classes((AllowAny,))
class MpesaCheckout(APIView):
    """Handles the initiation of MPESA checkout.

    Args:
        APIView (class): Django REST framework class for API views.
    """
    serializer = MpesaCheckoutSerializer

    def post(self, request, *args, **kwargs):
        """Initiates the MPESA checkout process.

        Args:
            request (Request): HTTP request object.

        Returns:
            JsonResponse: JSON response indicating the result of the
            MPESA checkout request.
        """
        serializer = self.serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            payload = {"data":serializer.validated_data, "request":request}
            res = gateway.stk_push_request(payload)
            return JsonResponse(res, status=200)


@authentication_classes([])
@permission_classes((AllowAny,))
class MpesaCallBack(APIView):
    """Handles callbacks from the MPESA payment system.

    Args:
        APIView (class): Django REST framework class for API views.
    """

    def get(self, request):
        """Handles GET requests for MPESA callback.

        Returns:
            Response: HTTP response indicating the status of the callback.
        """
        return Response({"status": "OK"}, status=200)

    def post(self, request, *args, **kwargs):
        """Handles POST requests for MPESA callback.

        Returns:
            JsonResponse: JSON response indicating the result of the MPESA callback processing.
        """
        logging.info("{}".format("Callback from MPESA"))
        data = request.body
        return gateway.callback_handler(json.loads(data))


class CheckTransactionStatus(APIView):
    """Handles checking the status of a transaction.

    Args:
        APIView (class): Django REST framework class for API views.
    """
    def get(self, request, *args, **kwargs):
        """Handles GET requests for checking transaction status.
        Returns:
            Response: JSON response indicating the transaction status.
        """
        checkout_request_id = self.request.query_params.get('checkout_request_id', None)

        if not checkout_request_id:
            return Response({"error": "checkout_request_id parameter is required."}, status=400)

        try:
            transaction = Transaction.objects.get(checkout_request_id=checkout_request_id)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found."}, status=404)

        transaction_data = TransactionSerializer(transaction).data
        return Response({"transaction_status": transaction_data["status"]})
