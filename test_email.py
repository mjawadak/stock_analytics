import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_send_email():
    # Email configuration - UPDATE THESE WITH YOUR DETAILS
    sender_email = "your_email@outlook.com"  # Replace with your email
    sender_password = "your_password"  # Replace with your password
    recipient_email = "recipient@example.com"  # Replace with recipient email
    
    # SMTP Configuration - Choose your provider:
    # Outlook/Hotmail
    smtp_server = "smtp-mail.outlook.com"
    smtp_port = 587
    
    # Yahoo Mail
    # smtp_server = "smtp.mail.yahoo.com"
    # smtp_port = 587
    
    # Apple iCloud
    # smtp_server = "smtp.mail.me.com"
    # smtp_port = 587
    
    # ProtonMail
    # smtp_server = "127.0.0.1"  # Requires ProtonMail Bridge
    # smtp_port = 1025
    
    # Email content
    subject = "Test Email from Python Script"
    body = """
    Hello!
    
    This is a test email sent from Python.
    If you're reading this, the email script is working correctly!
    
    Best regards,
    Your Trading App
    """
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    # Add body to email
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # SMTP server connection
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable TLS encryption
        server.login(sender_email, sender_password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print("✅ Email sent successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

if __name__ == '__main__':
    print("Testing email sending...")
    test_send_email()
