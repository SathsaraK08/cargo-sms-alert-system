import httpx
from typing import Dict, Any, Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class SMSService:
    def __init__(self):
        self.api_key = settings.INFOBIP_API_KEY
        self.base_url = settings.INFOBIP_BASE_URL
        self.headers = {
            "Authorization": f"App {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def send_sms(
        self,
        to: str,
        message: str,
        from_number: str = "CargoSMS",
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Send SMS using Infobip API
        
        Args:
            to: Recipient phone number (with country code)
            message: SMS message content
            from_number: Sender ID
            language: Language code (en, si, ta)
            
        Returns:
            Dict with response data
        """
        if not self.api_key:
            logger.warning("SMS API key not configured, simulating SMS send")
            return {
                "status": "simulated",
                "message": f"SMS to {to}: {message}",
                "language": language
            }

        url = f"{self.base_url}/sms/2/text/advanced"
        
        payload = {
            "messages": [
                {
                    "from": from_number,
                    "destinations": [{"to": to}],
                    "text": message,
                    "language": {"languageCode": language}
                }
            ]
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, 
                    json=payload, 
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                
                result = response.json()
                logger.info(f"SMS sent successfully to {to}")
                return result
                
        except httpx.HTTPError as e:
            logger.error(f"Failed to send SMS to {to}: {e}")
            return {
                "status": "error",
                "error": str(e),
                "message": message,
                "to": to
            }

    async def send_package_alert(
        self,
        phone: str,
        tracking_id: str,
        status: str,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Send package status alert SMS
        
        Args:
            phone: Recipient phone number
            tracking_id: Package tracking ID
            status: Package status
            language: Language preference
            
        Returns:
            SMS send result
        """
        templates = {
            "en": {
                "registered": f"Your package {tracking_id} has been registered and is being processed.",
                "in_transit": f"Your package {tracking_id} is now in transit.",
                "delivered": f"Your package {tracking_id} has been delivered successfully.",
                "delayed": f"Your package {tracking_id} has been delayed. We apologize for the inconvenience.",
            },
            "si": {
                "registered": f"ඔබේ පැකේජය {tracking_id} ලියාපදිංචි කර ඇති අතර සැකසෙමින් පවතී.",
                "in_transit": f"ඔබේ පැකේජය {tracking_id} දැන් ප්‍රවාහනයේ පවතී.",
                "delivered": f"ඔබේ පැකේජය {tracking_id} සාර්ථකව බෙදා හරින ලදී.",
                "delayed": f"ඔබේ පැකේජය {tracking_id} ප්‍රමාද වී ඇත. අපි අපහසුතාවයට කණගාටු වෙමු.",
            },
            "ta": {
                "registered": f"உங்கள் பொதி {tracking_id} பதிவு செய்யப்பட்டு செயலாக்கப்படுகிறது.",
                "in_transit": f"உங்கள் பொதி {tracking_id} இப்போது போக்குவரத்தில் உள்ளது.",
                "delivered": f"உங்கள் பொதி {tracking_id} வெற்றிகரமாக வழங்கப்பட்டது.",
                "delayed": f"உங்கள் பொதி {tracking_id} தாமதமாகிவிட்டது. அசௌகரியத்திற்கு வருந்துகிறோம்.",
            }
        }
        
        message = templates.get(language, templates["en"]).get(
            status, f"Package {tracking_id} status update: {status}"
        )
        
        return await self.send_sms(phone, message, language=language)


sms_service = SMSService()
