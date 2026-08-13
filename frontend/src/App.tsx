import { useState } from "react";
import Register from "./pages/Register";
import Login from "./pages/login";
import Dashboard from "./pages/Dashboard";
import "./App.css";

function App() {
  const [page, setPage] = useState("login");

  return (
    <div className="app-container">

      <div className="nav-buttons">
        <button onClick={() => setPage("login")}>
          Login
        </button>

        <button onClick={() => setPage("register")}>
          Register
        </button>

        <button onClick={() => setPage("dashboard")}>
          Dashboard
        </button>
      </div>

      {page === "login" && <Login />}
      {page === "register" && <Register />}
      {page === "dashboard" && <Dashboard />}

    </div>
  );
}

export default App;