// PhoneLogin.jsx
import React, { useState } from 'react';

const PhoneLogin = () => {
  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [token, setToken] = useState('');

  // API call to backend
  const apiCall = async (endpoint, method, body = null) => {
    const res = await fetch(`/api${endpoint}`, {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` })
      },
      body: JSON.stringify(body)
    });
    return res.json();
  };

  const handlePhoneSubmit = async (e) => {
    e.preventDefault();
    try {
      await apiCall('/register', 'POST', { phone, password: 'temp' });
      await apiCall('/otp/request', 'POST', { phone });
      alert('OTP sent to your phone');
    } catch (error) {
      alert(error.message);
    }
  };

  const handleOtpSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await apiCall('/otp/verify', 'POST', { phone, otp });
      setToken(data.token);
      setIsLoggedIn(true);
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <div>
      {!isLoggedIn ? (
        <form onSubmit={handlePhoneSubmit}>
          <input 
            type="tel" 
            value={phone} 
            onChange={(e) => setPhone(e.target.value)}
            placeholder="Enter phone number"
            required
          />
          <button type="submit">Send OTP</button>
        </form>
      ) : (
        <form onSubmit={handleOtpSubmit}>
          <input 
            type="text" 
            value={otp} 
            onChange={(e) => setOtp(e.target.value)}
            placeholder="Enter OTP"
            required
          />
          <button type="submit">Login</button>
        </form>
      )}
    </div>
  );
};

export default PhoneLogin;
