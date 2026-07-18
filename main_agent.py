import os
import sys
import time
from datetime import datetime

print("🤖 SHAHID'S PERSONAL AI AGENT")
print("="*50)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Step 1 - File Organizer
print("\n📁 Step 1: File Organizer...")
exec(open('file_organizer.py').read())
print("✅ Files organized!")
time.sleep(2)

# Step 2 - Email Manager
print("\n📧 Step 2: Email Manager...")
exec(open('email_manager.py').read())
print("✅ Emails analyzed!")
time.sleep(2)

# Step 3 - Job Finder
print("\n💼 Step 3: Job Finder...")
exec(open('job_finder.py').read())
print("✅ Jobs found!")
time.sleep(2)

# Step 4 - WhatsApp
print("\n📱 Step 4: WhatsApp Notifier...")
exec(open('whatsapp_notifier.py').read())
print("✅ WhatsApp sent!")

print("\n🎉 Daily AI Agent Complete!")
print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")