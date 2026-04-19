import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email(
    sender_email,
    sender_password,
    recipient_email,
    subject,
    body,
    is_html=False,
    attachment_path=None,
    smtp_server="smtp.gmail.com",
    smtp_port=587
):
    """
    Send an email with optional HTML content and attachments.
    
    Args:
        sender_email: Sender's email address
        sender_password: Sender's email password or app password
        recipient_email: Recipient's email address (can be a list)
        subject: Email subject
        body: Email body content
        is_html: Whether the body is HTML (default: False)
        attachment_path: Path to file to attach (optional)
        smtp_server: SMTP server (default: Gmail)
        smtp_port: SMTP port (default: 587 for TLS)
    """
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email if isinstance(recipient_email, str) else ", ".join(recipient_email)
    msg['Subject'] = subject
    
    # Add body to email
    if is_html:
        msg.attach(MIMEText(body, 'html'))
    else:
        msg.attach(MIMEText(body, 'plain'))
    
    # Add attachment if provided
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {os.path.basename(attachment_path)}'
        )
        msg.attach(part)
    
    try:
        # Create SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable TLS encryption
        server.login(sender_email, sender_password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print(f"Email sent successfully to {recipient_email}")
        return True
        
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_trading_alert(symbol, price, action, recipient_email):
    """
    Send a trading alert email for stock price changes.
    """
    subject = f"Trading Alert: {symbol}"
    body = f"""
    Stock Trading Alert
    
    Symbol: {symbol}
    Current Price: ${price}
    Recommended Action: {action}
    
    This is an automated alert from your trading app.
    """
    
    # Use environment variables for email credentials
    sender_email = os.getenv('EMAIL_USER', 'your_email@gmail.com')
    sender_password = os.getenv('EMAIL_PASSWORD', 'your_app_password')
    
    return send_email(sender_email, sender_password, recipient_email, subject, body)

def main():
    # Example usage
    sender_email = "your_email@gmail.com"  # Replace with your email
    sender_password = "your_app_password"  # Replace with your app password
    recipient_email = "recipient@example.com"  # Replace with recipient email
    
    subject = "Test Email from Trading App"
    body = """
    Hello,
    
    This is a test email from your trading application.
    
    Best regards,
    Trading Bot
    """
    
    # Send plain text email
    success = send_email(sender_email, sender_password, recipient_email, subject, body)
    
    if success:
        print("Test email sent successfully!")
    else:
        print("Failed to send test email.")

if __name__ == '__main__':
    main()
