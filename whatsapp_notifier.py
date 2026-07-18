import pywhatkit as kit
import json
import time
from datetime import datetime


# SHAHID'S WHATSAPP NOTIFIER


# Mee WhatsApp number (with country code)
YOUR_NUMBER = "+919676522753"

def send_whatsapp_message(phone_number, message):
    """Send WhatsApp message"""
    try:
        now = datetime.now()
        # Send after 2 minutes
        hour = now.hour
        minute = now.minute + 2
        
        if minute >= 60:
            hour += 1
            minute -= 60
        
        print(f"📱 Sending WhatsApp message at {hour}:{minute:02d}...")
        
        kit.sendwhatmsg(
            phone_number,
            message,
            hour,
            minute,
            wait_time=20,
            tab_close=True
        )
        
        print("✅ WhatsApp message sent!")
        return True
        
    except Exception as e:
        print(f"❌ Error sending: {e}")
        return False

def load_job_report():
    """Load job report"""
    try:
        with open('job_report.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return None

def load_email_summary():
    """Load email summary"""
    try:
        with open('email_summary.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return None

def create_daily_summary():
    """Create combined daily summary"""
    now = datetime.now().strftime('%d %b %Y, %I:%M %p')
    
    summary = f" *Shahid's Daily AI Agent Report*\n"
    summary += f"{now}\n"
    summary += f"{'='*35}\n\n"
    
    # Email summary
    email_summary = load_email_summary()
    if email_summary:
        summary += " *EMAIL SUMMARY:*\n"
        # Get just the totals
        lines = email_summary.split('\n')
        for line in lines:
            if 'Total' in line or 'Important' in line or 'Spam' in line:
                summary += f"{line}\n"
        summary += "\n"
    
    # Job summary
    job_report = load_job_report()
    if job_report:
        summary += " *JOB SUMMARY:*\n"
        lines = job_report.split('\n')
        for line in lines[:20]:  # First 20 lines
            if line.strip():
                summary += f"{line}\n"
    
    summary += f"\n{'='*35}\n"
    summary += " *Have a productive day Shahid!*"
    
    return summary

def main():
    print(" SHAHID'S WHATSAPP NOTIFIER")
    print("="*50)
    
    # Create daily summary
    summary = create_daily_summary()
    
    print("\n Summary to send:")
    print(summary)
    print("\n" + "="*50)
    
    # Confirm before sending
    confirm = input("\n WhatsApp lo pamputava? (y/n): ")
    
    if confirm.lower() == 'y':
        print("\n  WhatsApp Web open avutundi...")
        print("  Browser lo WhatsApp Web logged in ga undi check cheyyi!")
        time.sleep(2)
        
        send_whatsapp_message(YOUR_NUMBER, summary)
    else:
        print(" Cancelled!")
        # Save summary anyway
        with open('daily_summary.txt', 'w', encoding='utf-8') as f:
            f.write(summary)
        print("✅ Saved to daily_summary.txt!")

if __name__ == "__main__":
    main()