import { useState } from "react";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";

function App() {
  const [loggedIn, setLoggedIn] = useState(
    !!localStorage.getItem("token")
  );

  const [showRegister, setShowRegister] = useState(false);

  if (loggedIn) {
    return <Dashboard />;
  }

  if (showRegister) {
    return (
      <Register
        onRegisterSuccess={() => setShowRegister(false)}
        onBackToLogin={() => setShowRegister(false)}
      />
    );
  }

  return (
    <Login
      onLogin={() => setLoggedIn(true)}
      onShowRegister={() => setShowRegister(true)}
    />
  );
}

export default App;