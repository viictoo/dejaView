import logging
import requests
from rest_framework.response import Response
from phonenumber_field.phonenumber import PhoneNumber

from .models import Transaction
from .serializers import TransactionSerializer

logging = logging.getLogger("default")
def get_status(data):
    try:
        status = data["Body"]["stkCallback"]["ResultCode"]
    except Exception as e:
        logging.error(f"Error: {e}")
        status = 1
    return status

def get_transaction_object(data):
    checkout_request_id = data["Body"]["stkCallback"]["CheckoutRequestID"]
    transaction, _ = Transaction.objects.get_or_create(
        checkout_request_id=checkout_request_id
    )

    return transaction

def handle_successful_pay(data, transaction):
    items = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]
    for item in items:
        if item["Name"] == "Amount":
            amount = item["Value"]
        elif item["Name"] == "MpesaReceiptNumber":
            receipt_no = item["Value"]
        elif item["Name"] == "PhoneNumber":
            phone_number = item["Value"]

    transaction.amount = amount
    transaction.phone_number = PhoneNumber(raw_input=phone_number)
    transaction.receipt_no = receipt_no
    transaction.confirmed = True

    return transaction

def callback_handler(data):
    status = get_status(data)
    transaction = get_transaction_object(data)
    if status==0:
        handle_successful_pay(data, transaction)
    else:
        transaction.status = 1

    transaction.status = status
    transaction.save()

    transaction_data = TransactionSerializer(transaction).data

    logging.info("Transaction completed info {}".format(transaction_data))

    return Response({"status": "ok", "code": 0}, status=200)
