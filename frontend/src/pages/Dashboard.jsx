
import { useEffect, useState } from "react";
import "../App.css";
import Sidebar from "../components/Sidebar";

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
    let cancelled = false;

    async function loadDashboard() {
      try {
        const [summaryData, donationsData] = await Promise.all([
          getDashboardSummary(),
          getDashboardDonations(),
        ]);

        if (!cancelled) {
          setDashboard(summaryData);
          setDonations(
            Array.isArray(donationsData) ? donationsData : []
          );
          setError("");
        }
      } catch (err) {
        console.error("Dashboard API error:", err);

        if (!cancelled) {
          setError("Unable to load SmartFood City dashboard.");
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadDashboard();

    return () => {
      cancelled = true;
    };
  }, []);

  if (loading) {
    return (
      <div className="loading">
        Loading SmartFood City...
      </div>
    );
  }

  if (error || !dashboard) {
    return (
      <div className="error">
        <h2>SmartFood City</h2>
        <p>{error || "Dashboard data is unavailable."}</p>
        <p>Make sure FastAPI is running on port 8000.</p>
        <button onClick={() => window.location.reload()}>
          Retry
        </button>
      </div>
    );
  }

  const stats = [
    {
      icon: "🏢",
      label: "Total Donors",
      value: dashboard.donors?.total ?? 0,
    },
    {
      icon: "🏠",
      label: "Receivers",
      value: dashboard.receivers?.total ?? 0,
    },
    {
      icon: "🍱",
      label: "Food Donations",
      value: dashboard.food_donations?.total ?? 0,
    },
    {
      icon: "🚴",
      label: "Volunteers",
      value: dashboard.volunteers?.total ?? 0,
    },
    {
      icon: "🚚",
      label: "Active Deliveries",
      value: dashboard.deliveries?.active ?? 0,
    },
    {
      icon: "✅",
      label: "Completed",
      value: dashboard.deliveries?.completed ?? 0,
    },
    {
      icon: "⚖️",
      label: "Food Saved",
      value: `${dashboard.impact?.food_saved_kg ?? 0} kg`,
    },
    {
      icon: "🍽️",
      label: "Meals Available",
      value: dashboard.impact?.meals_available ?? 0,
    },
  ];

  return (
    <div className="app">
      {/* Reusable Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <main className="main-content">
        {/* Header */}
        <header className="topbar">
          <div>
            <h1>Dashboard</h1>
            <p>SmartFood City overview</p>
          </div>

          <button
            className="notification"
            type="button"
            aria-label="Notifications"
            title="Notifications"
          >
            🔔
          </button>
        </header>

        {/* Statistics */}
        <section className="stats-grid">
          {stats.map((stat) => (
            <div className="stat-card" key={stat.label}>
              <div className="stat-icon">{stat.icon}</div>

              <div>
                <p>{stat.label}</p>
                <h2>{stat.value}</h2>
              </div>
            </div>
          ))}
        </section>

        {/* Recent Activity */}
        <section className="content-grid">
          {/* Recent Food Donations */}
          <div className="panel">
            <div className="panel-header">
              <h2>Recent Food Donations</h2>
              <button type="button">View All</button>
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
                  <div className="food-icon">🍛</div>

                  <div className="food-info">
                    <strong>{donation.food_name}</strong>
                    <span>
                      {donation.donor_name || "Unknown Donor"}
                    </span>
                  </div>

                  <div className="food-quantity">
                    <strong>{donation.quantity_kg} kg</strong>
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
                    {donation.safety_status || "pending"}
                  </span>
                </div>
              ))
            )}
          </div>

          {/* Delivery Status */}
          <div className="panel">
            <div className="panel-header">
              <h2>Delivery Status</h2>
              <button type="button">View All</button>
            </div>

            <div className="delivery-status">
              <div className="status-item">
                <span className="status-dot completed" />

                <div>
                  <strong>Completed Deliveries</strong>
                  <span>
                    {dashboard.deliveries?.completed ?? 0}{" "}
                    {(dashboard.deliveries?.completed ?? 0) === 1
                      ? "delivery"
                      : "deliveries"}
                  </span>
                </div>
              </div>

              <div className="status-item">
                <span className="status-dot active-dot" />

                <div>
                  <strong>Active Deliveries</strong>
                  <span>
                    {dashboard.deliveries?.active ?? 0}{" "}
                    {(dashboard.deliveries?.active ?? 0) === 1
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
