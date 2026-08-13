import { useEffect, useState } from "react";
import "./Dashboard.css";

function Dashboard() {
  const [users, setUsers] = useState<any[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/users")
      .then((res) => res.json())
      .then((data) => {
        console.log("Users API:", data);
        setUsers(data.data);
      })
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="dashboard-container">

  <h1 className="dashboard-title">
    🔐 Face Recognition Dashboard
  </h1>

  <h2 className="dashboard-count">
    👥 Total Registered Users: {users.length}
  </h2>

  <div className="user-list">
    {users.map((user: any) => (
      <div key={user.id} className="user-card">
    
            <h3>
              {user.first_name} {user.last_name}
            </h3>

            <p>📧 {user.email}</p>
            <p> Age: {user.age}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Dashboard;