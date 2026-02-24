import re
import hashlib
import secrets
from datetime import datetime, timedelta

class PhoneNumberLogin:
    def __init__(self):
        self.users = {}  # Store users in memory (use DB in production)
        self.active_sessions = {}
    
    def validate_phone(self, phone):
        """Validate phone number format"""
        pattern = r'^\+?1?\d{9,15}$'
        return bool(re.match(pattern, phone))
    
    def generate_otp(self):
        """Generate 6-digit OTP"""
        return str(secrets.randbelow(900000) + 100000)
    
    def send_sms(self, phone, otp):
        """Simulate sending SMS (in production use Twilio/Firebase)"""
        print(f"SMS sent to {phone}: Your verification code is {otp}")
    
    def register_user(self, phone, password=None):
        """Register new user with phone number"""
        if not self.validate_phone(phone):
            raise ValueError("Invalid phone number")
        
        if phone in self.users:
            raise ValueError("Phone already registered")
        
        user_id = hashlib.sha256(phone.encode()).hexdigest()[:16]
        self.users[phone] = {
            "id": user_id,
            "password_hash": hashlib.sha256(password.encode()).hexdigest() if password else None,
            "created_at": datetime.now(),
            "last_login": None
        }
        return user_id
    
    def request_otp(self, phone):
        """Request OTP for phone number"""
        if phone not in self.users:
            raise ValueError("User not found")
        
        otp = self.generate_otp()
        self.send_sms(phone, otp)
        self.active_sessions[phone] = {
            "otp": otp,
            "expires_at": datetime.now() + timedelta(minutes=10)
        }
        return True
    
    def verify_otp(self, phone, otp):
        """Verify OTP for phone number"""
        if phone not in self.active_sessions:
            raise ValueError("No active session")
        
        session = self.active_sessions[phone]
        if datetime.now() > session["expires_at"]:
            del self.active_sessions[phone]
            raise ValueError("OTP expired")
        
        if session["otp"] != otp:
            raise ValueError("Invalid OTP")
        
        # Clean up session
        del self.active_sessions[phone]
        
        # Update last login
        self.users[phone]["last_login"] = datetime.now()
        return self.users[phone]["id"]
    
    def login_with_phone(self, phone, password=None):
        """Login using phone number"""
        if phone not in self.users:
            raise ValueError("User not found")
        
        user = self.users[phone]
        
        # If password provided, verify it
        if password and user["password_hash"] != hashlib.sha256(password.encode()).hexdigest():
            raise ValueError("Invalid credentials")
        
        # Generate session token
        token = secrets.token_hex(32)
        return {
            "token": token,
            "user_id": user["id"],
            "user_data": {
                "phone": phone,
                "created_at": user["created_at"],
                "last_login": user["last_login"]
            }
        }

# Example usage
login_system = PhoneNumberLogin()

# Register user
try:
    user_id = login_system.register_user("+1234567890", "securepassword123")
    print(f"Registered user with ID: {user_id}")
    
    # Request OTP
    login_system.request_otp("+1234567890")
    
    # Verify OTP (replace with actual received OTP)
    token_data = login_system.verify_otp("+1234567890", "123456")  # Replace with actual OTP
    print(f"Login successful! Token: {token_data['token']}")
    
except Exception as e:
    print(f"Error: {e}")
