import { useEffect, useState } from "react";
import "../App.css";

import {
  getDashboardSummary,
  getDashboardDonations,
} from "../services/api";

function Dashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [donations, setDonations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      getDashboardSummary(),
      getDashboardDonations(),
    ])
      .then(([summaryData, donationsData]) => {
        console.log("Dashboard data:", summaryData);
        console.log("Donation data:", donationsData);

        setDashboard(summaryData);
        setDonations(donationsData);
        setLoading(false);
      })
      .catch((err) => {
        console.error("API Error:", err);
        setError("Unable to connect to SmartFood API");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="loading">
        Loading SmartFood City...
      </div>
    );
  }

  if (error) {
    return (
      <div className="error">
        <h2>SmartFood City</h2>
        <p>{error}</p>
        <p>Make sure FastAPI is running on port 8000.</p>
      </div>
    );
  }

  return (
    <div className="app">

      {/* Sidebar */}
      <aside className="sidebar">

        <div className="logo">
          <div className="logo-icon">🍲</div>

          <div>
            <h2>SmartFood</h2>
            <span>City</span>
          </div>
        </div>

        <nav>
          <a className="active">📊 Dashboard</a>
          <a>🏢 Donors</a>
          <a>🏠 Receivers</a>
          <a>🍱 Food Donations</a>
          <a>🚴 Volunteers</a>
          <a>🚚 Deliveries</a>
          <a>⚙️ Settings</a>
        </nav>

        <div className="sidebar-bottom">
          <div className="admin-profile">

            <div className="avatar">
              A
            </div>

            <div>
              <strong>Administrator</strong>
              <small>Admin</small>
            </div>

          </div>
        </div>

      </aside>

      {/* Main Content */}
      <main className="main-content">

        {/* Header */}
        <header className="topbar">

          <div>
            <h1>Dashboard</h1>
            <p>SmartFood City overview</p>
          </div>

          <button className="notification">
            🔔
          </button>

        </header>

        {/* Statistics */}
        <section className="stats-grid">

          <div className="stat-card">
            <div className="stat-icon">🏢</div>

            <div>
              <p>Total Donors</p>
              <h2>{dashboard.donors.total}</h2>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🏠</div>

            <div>
              <p>Receivers</p>
              <h2>{dashboard.receivers.total}</h2>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🍱</div>

            <div>
              <p>Food Donations</p>
              <h2>{dashboard.food_donations.total}</h2>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🚴</div>

            <div>
              <p>Volunteers</p>
              <h2>{dashboard.volunteers.total}</h2>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🚚</div>

            <div>
              <p>Active Deliveries</p>
              <h2>{dashboard.deliveries.active}</h2>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">✅</div>

            <div>
              <p>Completed</p>
              <h2>{dashboard.deliveries.completed}</h2>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">⚖️</div>

            <div>
              <p>Food Saved</p>
              <h2>
                {dashboard.impact.food_saved_kg} kg
              </h2>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🍽️</div>

            <div>
              <p>Meals Available</p>
              <h2>
                {dashboard.impact.meals_available}
              </h2>
            </div>
          </div>

        </section>

        {/* Recent Activity */}
        <section className="content-grid">

          {/* Recent Food Donations */}
          <div className="panel">

            <div className="panel-header">
              <h2>Recent Food Donations</h2>
              <button>View All</button>
            </div>

            {donations.length === 0 ? (

              <div className="empty-state">
                No food donations available.
              </div>

            ) : (

              donations.slice(0, 5).map((donation) => (

                <div
                  className="donation-row"
                  key={donation.id}
                >

                  <div className="food-icon">
                    🍛
                  </div>

                  <div className="food-info">

                    <strong>
                      {donation.food_name}
                    </strong>

                    <span>
                      {donation.donor_name || "Unknown Donor"}
                    </span>

                  </div>

                  <div className="food-quantity">

                    <strong>
                      {donation.quantity_kg} kg
                    </strong>

                    <span>
                      {donation.estimated_meals} meals
                    </span>

                  </div>

                  <span
                    className={`status ${
                      donation.safety_status === "approved"
                        ? "approved"
                        : ""
                    }`}
                  >
                    {donation.safety_status}
                  </span>

                </div>

              ))

            )}

          </div>

          {/* Delivery Status */}
          <div className="panel">

            <div className="panel-header">
              <h2>Delivery Status</h2>
              <button>View All</button>
            </div>

            <div className="delivery-status">

              <div className="status-item">

                <span className="status-dot completed"></span>

                <div>
                  <strong>
                    Completed Deliveries
                  </strong>

                  <span>
                    {dashboard.deliveries.completed}{" "}
                    {dashboard.deliveries.completed === 1
                      ? "delivery"
                      : "deliveries"}
                  </span>
                </div>

              </div>

              <div className="status-item">

                <span className="status-dot active-dot"></span>

                <div>
                  <strong>
                    Active Deliveries
                  </strong>

                  <span>
                    {dashboard.deliveries.active}{" "}
                    {dashboard.deliveries.active === 1
                      ? "delivery"
                      : "deliveries"}
                  </span>
                </div>

              </div>

            </div>

          </div>

        </section>

      </main>

    </div>
  );
}

export default Dashboard;