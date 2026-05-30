import { useState } from "react";
import api from "../services/api";

function Register({ onRegisterSuccess, onBackToLogin }) {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      await api.post("/register", {
        full_name: fullName,
        email,
        password,
      });

      alert("Registration successful. Please login.");
      onRegisterSuccess();
    } catch (error) {
      alert("Registration failed");
      console.error(error);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="bg-slate-800 p-8 rounded-2xl shadow-xl w-full max-w-md">
        <h1 className="text-3xl font-bold text-white text-center mb-6">
          Create Account
        </h1>

        <form onSubmit={handleRegister}>
          <input
            type="text"
            placeholder="Full Name"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            className="w-full p-3 rounded-lg bg-slate-700 text-white mb-4 border border-slate-600"
          />

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full p-3 rounded-lg bg-slate-700 text-white mb-4 border border-slate-600"
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-3 rounded-lg bg-slate-700 text-white mb-6 border border-slate-600"
          />

          <button
            type="submit"
            className="w-full bg-blue-600 py-3 rounded-lg hover:bg-blue-700 text-white font-semibold"
          >
            Register
          </button>
        </form>

        <button
          onClick={onBackToLogin}
          className="w-full mt-4 text-slate-300 hover:text-white"
        >
          Already have an account? Login
        </button>
      </div>
    </div>
  );
}

export default Register;