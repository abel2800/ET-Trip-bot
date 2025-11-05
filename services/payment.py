"""Payment processing service for TeleBirr and CBE Birr."""

import requests
import hashlib
import json
import logging
from typing import Dict, Any, Optional
from enum import Enum

from config.settings import settings

logger = logging.getLogger(__name__)


class PaymentMethod(Enum):
    """Supported payment methods."""
    TELEBIRR = "TeleBirr"
    CBE_BIRR = "CBE Birr"


class PaymentStatus(Enum):
    """Payment transaction status."""
    PENDING = "Pending"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"


class PaymentProcessor:
    """Service for processing payments via Ethiopian payment gateways."""
    
    def __init__(self):
        self.telebirr_api_key = settings.TELEBIRR_API_KEY
        self.telebirr_api_secret = settings.TELEBIRR_API_SECRET
        self.telebirr_api_url = settings.TELEBIRR_API_URL
        
        self.cbe_api_key = settings.CBE_BIRR_API_KEY
        self.cbe_api_secret = settings.CBE_BIRR_API_SECRET
        self.cbe_api_url = settings.CBE_BIRR_API_URL
    
    def initiate_payment(
        self,
        method: PaymentMethod,
        amount: float,
        user_id: int,
        booking_reference: str,
        phone_number: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Initiate a payment transaction.
        
        Args:
            method: Payment method to use
            amount: Amount to charge in ETB
            user_id: Telegram user ID
            booking_reference: Booking reference number
            phone_number: User's phone number (required for some methods)
        
        Returns:
            Payment initiation response
        """
        if method == PaymentMethod.TELEBIRR:
            return self._initiate_telebirr_payment(
                amount, user_id, booking_reference, phone_number
            )
        elif method == PaymentMethod.CBE_BIRR:
            return self._initiate_cbe_payment(
                amount, user_id, booking_reference
            )
        else:
            return {
                "success": False,
                "error": "Unsupported payment method"
            }
    
    def _initiate_telebirr_payment(
        self,
        amount: float,
        user_id: int,
        booking_reference: str,
        phone_number: Optional[str]
    ) -> Dict[str, Any]:
        """
        Initiate TeleBirr payment.
        
        Args:
            amount: Amount in ETB
            user_id: User ID
            booking_reference: Booking reference
            phone_number: Phone number for payment
        
        Returns:
            Payment response
        """
        if not self.telebirr_api_url:
            # Mock response for development
            return {
                "success": True,
                "transaction_id": f"TB_{booking_reference}",
                "payment_url": f"https://telebirr.com/pay?ref={booking_reference}",
                "qr_code": "mock_qr_code_data",
                "status": PaymentStatus.PENDING.value,
                "message": "Please complete payment via TeleBirr app"
            }
        
        try:
            payload = {
                "api_key": self.telebirr_api_key,
                "amount": amount,
                "currency": "ETB",
                "reference": booking_reference,
                "phone": phone_number,
                "user_id": str(user_id),
                "callback_url": f"https://yourbot.com/callback/payment/{booking_reference}"
            }
            
            # Generate signature
            payload["signature"] = self._generate_signature(payload, self.telebirr_api_secret)
            
            response = requests.post(
                f"{self.telebirr_api_url}/payment/initiate",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            return response.json()
        
        except requests.RequestException as e:
            logger.error(f"TeleBirr payment initiation error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _initiate_cbe_payment(
        self,
        amount: float,
        user_id: int,
        booking_reference: str
    ) -> Dict[str, Any]:
        """
        Initiate CBE Birr payment.
        
        Args:
            amount: Amount in ETB
            user_id: User ID
            booking_reference: Booking reference
        
        Returns:
            Payment response
        """
        if not self.cbe_api_url:
            # Mock response for development
            return {
                "success": True,
                "transaction_id": f"CBE_{booking_reference}",
                "payment_url": f"https://cbebirr.et/pay?ref={booking_reference}",
                "account_number": "1000123456789",
                "status": PaymentStatus.PENDING.value,
                "message": "Please transfer to the provided account"
            }
        
        try:
            payload = {
                "api_key": self.cbe_api_key,
                "amount": amount,
                "currency": "ETB",
                "reference": booking_reference,
                "user_id": str(user_id)
            }
            
            # Generate signature
            payload["signature"] = self._generate_signature(payload, self.cbe_api_secret)
            
            response = requests.post(
                f"{self.cbe_api_url}/payment/create",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            return response.json()
        
        except requests.RequestException as e:
            logger.error(f"CBE Birr payment initiation error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def check_payment_status(
        self,
        transaction_id: str,
        method: PaymentMethod
    ) -> Dict[str, Any]:
        """
        Check the status of a payment transaction.
        
        Args:
            transaction_id: Transaction identifier
            method: Payment method used
        
        Returns:
            Payment status information
        """
        if method == PaymentMethod.TELEBIRR:
            return self._check_telebirr_status(transaction_id)
        elif method == PaymentMethod.CBE_BIRR:
            return self._check_cbe_status(transaction_id)
        else:
            return {
                "success": False,
                "error": "Unsupported payment method"
            }
    
    def _check_telebirr_status(self, transaction_id: str) -> Dict[str, Any]:
        """Check TeleBirr payment status."""
        if not self.telebirr_api_url:
            # Mock response
            return {
                "success": True,
                "transaction_id": transaction_id,
                "status": PaymentStatus.COMPLETED.value,
                "amount": 1000.00
            }
        
        try:
            response = requests.get(
                f"{self.telebirr_api_url}/payment/status/{transaction_id}",
                headers={"Authorization": f"Bearer {self.telebirr_api_key}"},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        
        except requests.RequestException as e:
            logger.error(f"TeleBirr status check error: {e}")
            return {"success": False, "error": str(e)}
    
    def _check_cbe_status(self, transaction_id: str) -> Dict[str, Any]:
        """Check CBE Birr payment status."""
        if not self.cbe_api_url:
            # Mock response
            return {
                "success": True,
                "transaction_id": transaction_id,
                "status": PaymentStatus.COMPLETED.value,
                "amount": 1000.00
            }
        
        try:
            response = requests.get(
                f"{self.cbe_api_url}/payment/status/{transaction_id}",
                headers={"Authorization": f"Bearer {self.cbe_api_key}"},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        
        except requests.RequestException as e:
            logger.error(f"CBE status check error: {e}")
            return {"success": False, "error": str(e)}
    
    def _generate_signature(self, payload: Dict[str, Any], secret: str) -> str:
        """
        Generate payment signature for authentication.
        
        Args:
            payload: Payment data
            secret: API secret key
        
        Returns:
            Signature string
        """
        # Sort and concatenate payload values
        sorted_items = sorted(payload.items())
        data_string = "".join([str(v) for k, v in sorted_items if k != 'signature'])
        signature_string = f"{secret}{data_string}{secret}"
        
        # Generate SHA256 hash
        signature = hashlib.sha256(signature_string.encode()).hexdigest()
        return signature


