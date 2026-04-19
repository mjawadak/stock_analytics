import requests
import json

def send_email_via_api(to_email, subject, message):
    """
    Send email using EmailJS (free service, no account signup needed for basic use)
    You just need to register at emailjs.com for a service ID
    """
    
    # EmailJS configuration (you'll need to register at emailjs.com)
    service_id = "your_service_id"  # Get from emailjs.com
    template_id = "your_template_id"  # Get from emailjs.com  
    user_id = "your_user_id"  # Get from emailjs.com
    
    url = "https://api.emailjs.com/api/v1.0/email/send"
    
    data = {
        "service_id": service_id,
        "template_id": template_id,
        "user_id": user_id,
        "template_params": {
            "to_email": to_email,
            "subject": subject,
            "message": message,
            "from_name": "Trading App"
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            print("✅ Email sent successfully!")
            return True
        else:
            print(f"❌ Failed to send email: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def send_webhook_notification(webhook_url, message):
    """
    Send notification via webhook (Discord, Slack, etc.)
    No email account needed!
    """
    
    data = {
        "content": message,  # For Discord
        "text": message     # For Slack
    }
    
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code in [200, 204]:
            print("✅ Webhook notification sent!")
            return True
        else:
            print(f"❌ Webhook failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def send_console_notification(message):
    """
    Simple console output - no external service needed
    """
    print("="*50)
    print("📧 NOTIFICATION")
    print("="*50)
    print(message)
    print("="*50)

# Example usage
if __name__ == '__main__':
    message = "AAPL stock price alert: $150.25 - Consider buying!"
    
    # Option 1: Console notification (works immediately)
    send_console_notification(message)
    
    # Option 2: Discord webhook (create a webhook in Discord server)
    # discord_webhook = "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
    # send_webhook_notification(discord_webhook, message)
    
    # Option 3: Slack webhook  
    # slack_webhook = "https://hooks.slack.com/services/YOUR_WEBHOOK_URL"
    # send_webhook_notification(slack_webhook, message)
