from .validators import validate_possible_number
from rest_framework import serializers

from . import models
from django.core.exceptions import ValidationError


class MpesaCheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = (
            "phone_number",
            "amount",
            "reference",
            "description",
            "video",
        )

    def validate_phone_number(self, phone_number):
        """A very Basic validation to remove the
        preceding + or replace the 0 with 254"""
        if phone_number[0] == "+":
            phone_number = phone_number[1:]
        if phone_number[0] == "0":
            phone_number = "254" + phone_number[1:]
        try:
            validate_possible_number(phone_number, "KE")
        except ValidationError:
            raise serializers.ValidationError(
                {"error": "Phone number is not valid"})

        return phone_number

    def validate_amount(self, amount):
        """this methods validates the amount"""
        if not amount or float(amount) <= 0:
            raise serializers.ValidationError(
                {"error": "Amount must be greater than Zero"}
            )
        return amount

    def validate_reference(self, reference):
        """Reference Validation"""
        if reference:
            return reference
        return "Test"

    def validate_description(self, description):
        """Description Validation"""
        if description:
            return description
        return "Test"

    def validate_video(self, video):
        """Video Data Validation"""
        if video:
            return video
        return "Test"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = "__all__"
