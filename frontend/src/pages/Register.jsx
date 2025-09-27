// frontend/src/pages/Register.jsx

import { useState } from 'react';
import axios from 'axios';

function Register() {
  const [form, setForm] = useState({
    name: '',
    email: '',
    message: ''
  });
  const [status, setStatus] = useState('');

  const handleChange = (e) => {
    setForm({...form, [e.target.name]: e.target.value});
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('https://backend-4q2p.onrender.com/submit', form);
      setStatus("Submitted! We'll contact you soon.");
      setForm({ name: '', email: '', message: '' });
    } catch (err) {
      setStatus("Submission failed. Please try again.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold mb-4">Register</h2>

        <label className="block mb-2">
          Name
          <input name="name" value={form.name} onChange={handleChange} required
            className="w-full p-2 border border-gray-300 rounded mt-1"/>
        </label>

        <label className="block mb-2">
          Email
          <input type="email" name="email" value={form.email} onChange={handleChange} required
            className="w-full p-2 border border-gray-400 rounded mt-1"/>
        </label>

        <label className="block mb-2">
          Message
          <textarea name="message" value={form.message} onChange={handleChange} required
            className="w-full p-2 border border-gray-300 rounded mt-1"/>
        </label>

        <button type="submit" className="w-full bg-blue-600 text-white p-2 mt-3 rounded hover:bg-blue-700">
          Submit
        </button>

        {status && <p className="text-green-700 mt-4">{status}</p>}
      </form>
    </div>
  );
}

export default Register;

