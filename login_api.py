from flask import Flask, request, jsonify
from login_system import PhoneNumberLogin

app = Flask(__name__)
login_system = PhoneNumberLogin()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    try:
        user_id = login_system.register_user(data['phone'], data.get('password'))
        return jsonify({"message": "User registered", "user_id": user_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/otp/request', methods=['POST'])
def request_otp():
    data = request.json
    try:
        login_system.request_otp(data['phone'])
        return jsonify({"message": "OTP sent"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/otp/verify', methods=['POST'])
def verify_otp():
    data = request.json
    try:
        token_data = login_system.verify_otp(data['phone'], data['otp'])
        return jsonify(token_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
