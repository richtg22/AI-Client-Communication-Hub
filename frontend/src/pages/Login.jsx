import { useState } from "react";
import api from "../services/api";

function Login({ onLogin, onShowRegister }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await api.post("/login", {
        email,
        password,
      });

      localStorage.setItem(
        "token",
        response.data.access_token
      );

      onLogin();
    } catch (error) {
      alert("Login failed");
      console.error(error);
    }
  };

  return (
  <div className="min-h-screen bg-slate-950 flex items-center justify-center">
    <div className="bg-slate-800 p-8 rounded-2xl shadow-xl w-full max-w-md">
      <h1 className="text-3xl font-bold text-white text-center mb-6">
        AI Client Communication Hub
      </h1>

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
        onClick={handleLogin}
        className="w-full bg-blue-600 py-3 rounded-lg hover:bg-blue-700 text-white font-semibold"
      >
        Login
      </button>

      <button
        onClick={onShowRegister}
        className="w-full mt-4 text-slate-300 hover:text-white"
        >
            New user? Create an account 
        </button>

    </div>
  </div>
);
}

export default Login;