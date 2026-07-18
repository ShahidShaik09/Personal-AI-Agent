import os
import base64
import json
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# SHAHID'S EMAIL MANAGER AGENT


SCOPES = ['https://mail.google.com/']

# My 4 Gmail accounts
EMAIL_ACCOUNTS = [
    'theshahidprofessional@gmail.com',
    'sunnyshahid1993@gmail.com',
    'shahidishan0909@gmail.com',
    'shahidsanjushaik@gmail.com'
]

# Keywords to identify important emails
IMPORTANT_KEYWORDS = [
    'job', 'interview', 'offer', 'hiring',
    'recruiter', 'opportunity', 'salary',
    'internship', 'shortlisted', 'selected',
    'application', 'resume', 'position',
    'data analyst', 'data scientist', 
    'joining', 'placement'
]

# Spam keywords
SPAM_KEYWORDS = [
    'lottery', 'winner', 'prize', 'click here',
    'free money', 'congratulations you won',
    'urgent', 'act now', 'limited time offer',
    'make money fast', 'work from home earn',
    'sale', 'bewagoofy', 'wallet expires',
    'discount', 'offer ends', 'bought this'
]

def authenticate_gmail(account_email, token_file):
    """Authenticate Gmail account"""
    creds = None
    
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)

def get_email_subject(service, msg_id):
    """Get email subject"""
    try:
        msg = service.users().messages().get(
            userId='me', id=msg_id, format='metadata',
            metadataHeaders=['Subject', 'From']
        ).execute()
        
        headers = msg['payload']['headers']
        subject = ''
        sender = ''
        
        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
            if header['name'] == 'From':
                sender = header['value']
        
        return subject, sender
    except:
        return 'No Subject', 'Unknown'

def is_spam(subject, sender):
    """Check if email is spam"""
    text = (subject + ' ' + sender).lower()
    return any(keyword in text for keyword in SPAM_KEYWORDS)

def is_important(subject, sender):
    """Check if email is job related/important"""
    text = (subject + ' ' + sender).lower()
    return any(keyword in text for keyword in IMPORTANT_KEYWORDS)

def analyze_account(account_email, service):
    """Analyze single Gmail account"""
    print(f"\n Analyzing: {account_email}")
    print("-" * 50)
    
    results = {
        'account': account_email,
        'total': 0,
        'spam': [],
        'important': [],
        'normal': 0
    }
    
    try:
        # Get unread emails
        msgs = service.users().messages().list(
            userId='me',
            labelIds=['INBOX'],
            q='is:unread',
            maxResults=20
        ).execute()
        
        messages = msgs.get('messages', [])
        results['total'] = len(messages)
        
        print(f" Unread emails: {len(messages)}")
        
        for msg in messages:
            subject, sender = get_email_subject(service, msg['id'])
            
            if is_spam(subject, sender):
                results['spam'].append({
                    'id': msg['id'],
                    'subject': subject,
                    'sender': sender
                })
                print(f"  SPAM: {subject[:50]}")
                
            elif is_important(subject, sender):
                results['important'].append({
                    'subject': subject,
                    'sender': sender
                })
                print(f" IMPORTANT: {subject[:50]}")
                
            else:
                results['normal'] += 1
        
        # Delete spam emails
        if results['spam']:
            print(f"\n  Deleting {len(results['spam'])} spam emails...")
            for spam in results['spam']:
                try:
                    service.users().messages().trash(
                        userId='me',
                        id=spam['id']
                    ).execute()
                    print(f" Deleted: {spam['subject'][:40]}")
                except:
                    print(f" Could not delete: {spam['subject'][:40]}")
        
    except Exception as e:
        print(f" Error: {e}")
    
    return results

def generate_summary(all_results):
    """Generate WhatsApp-ready summary"""
    print("\n" + "=" * 50)
    print(" EMAIL SUMMARY REPORT")
    print("=" * 50)
    print(f" {datetime.now().strftime('%d %b %Y, %I:%M %p')}")
    print()
    
    total_emails = 0
    total_spam = 0
    total_important = 0
    
    summary_text = f" *Email Summary - {datetime.now().strftime('%d %b %Y')}*\n\n"
    
    for result in all_results:
        total_emails += result['total']
        total_spam += len(result['spam'])
        total_important += len(result['important'])
        
        account_short = result['account'].split('@')[0]
        summary_text += f"  *{account_short}*\n"
        summary_text += f"   Total: {result['total']} unread\n"
        summary_text += f"    Important: {len(result['important'])}\n"
        summary_text += f"    Spam deleted: {len(result['spam'])}\n\n"
        
        if result['important']:
            summary_text += "   *Important emails:*\n"
            for imp in result['important'][:3]:
                summary_text += f"   • {imp['subject'][:40]}\n"
            summary_text += "\n"
    
    summary_text += f" *Total Summary*\n"
    summary_text += f"Total unread: {total_emails}\n"
    summary_text += f" Important: {total_important}\n"
    summary_text += f" Spam deleted: {total_spam}\n"
    
    print(summary_text)
    
    # Save summary to file
    with open('email_summary.txt', 'w', encoding='utf-8') as f:
        f.write(summary_text)
    
    print("\n Summary saved to email_summary.txt")
    print(" Copy this and send to WhatsApp!")
    
    return summary_text

def main():
    print(" SHAHID'S EMAIL MANAGER AGENT")
    print("=" * 50)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_results = []
    
    for i, account in enumerate(EMAIL_ACCOUNTS):
        token_file = f'token_{i}.json'
        
        try:
            print(f"\n Authenticating: {account}")
            service = authenticate_gmail(account, token_file)
            result = analyze_account(account, service)
            all_results.append(result)
            
        except Exception as e:
            print(f" Failed for {account}: {e}")
            all_results.append({
                'account': account,
                'total': 0,
                'spam': [],
                'important': [],
                'normal': 0
            })
    
    generate_summary(all_results)
    print("\n Email Manager Agent Complete!")

if __name__ == "__main__":
    main()