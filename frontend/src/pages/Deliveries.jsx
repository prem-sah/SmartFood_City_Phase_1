
import { useEffect, useState } from "react";
import "../App.css";
import Sidebar from "../components/Sidebar";

const API_BASE_URL = "http://127.0.0.1:8000";

function Deliveries({ currentPage, onNavigate }) {
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");

  useEffect(() => {
    let cancelled = false;

    async function loadAssignments() {
      try {
        const response = await fetch(`${API_BASE_URL}/assignments/`);

        if (!response.ok) {
          throw new Error("Failed to load assignments");
        }

        const data = await response.json();

        if (!cancelled) {
          setAssignments(Array.isArray(data) ? data : []);
          setError("");
        }
      } catch (err) {
        console.error("Deliveries API error:", err);

        if (!cancelled) {
          setError(
            "Unable to load deliveries. Check that FastAPI is running."
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadAssignments();

    return () => {
      cancelled = true;
    };
  }, []);

  function formatDate(value) {
    if (!value) return "—";

    const date = new Date(value);

    return Number.isNaN(date.getTime())
      ? value
      : date.toLocaleString();
  }

  function getStatusStyle(status) {
    const normalized = (status || "pending")
      .toLowerCase()
      .replaceAll(" ", "_");

    const styles = {
      completed: {
        background: "#dcfce7",
        color: "#166534",
      },
      in_transit: {
        background: "#dbeafe",
        color: "#1d4ed8",
      },
      picked_up: {
        background: "#ede9fe",
        color: "#6d28d9",
      },
      pending: {
        background: "#fef3c7",
        color: "#92400e",
      },
    };

    return {
      ...(styles[normalized] || {
        background: "#f1f5f9",
        color: "#475569",
      }),
      padding: "6px 10px",
      borderRadius: "999px",
      fontSize: "12px",
      fontWeight: 600,
      whiteSpace: "nowrap",
      display: "inline-block",
    };
  }

  // Filter assignments according to the selected status.
  const filteredAssignments = assignments.filter((assignment) => {
    const status = (assignment.status || "pending")
      .toLowerCase()
      .replaceAll(" ", "_");

    return statusFilter === "all" || status === statusFilter;
  });

  return (
    <div className="app">
      <Sidebar
        currentPage={currentPage}
        onNavigate={onNavigate}
      />

      <main className="main-content">
        <header className="topbar">
          <div>
            <h1>Deliveries</h1>
            <p>Track food pickups and delivery progress</p>
          </div>
        </header>

        <section className="panel">
          <div className="panel-header">
            <h2>Food Assignments</h2>

            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "12px",
                flexWrap: "wrap",
              }}
            >
              <label htmlFor="delivery-status-filter">
                Filter:
              </label>

              <select
                id="delivery-status-filter"
                value={statusFilter}
                onChange={(event) =>
                  setStatusFilter(event.target.value)
                }
                style={{
                  padding: "9px 12px",
                  border: "1px solid #d1d5db",
                  borderRadius: "8px",
                  background: "#ffffff",
                  color: "#374151",
                  cursor: "pointer",
                }}
              >
                <option value="all">All Statuses</option>
                <option value="pending">Pending</option>
                <option value="picked_up">Picked Up</option>
                <option value="in_transit">In Transit</option>
                <option value="completed">Completed</option>
              </select>

              <span>
                {filteredAssignments.length}{" "}
                {filteredAssignments.length === 1
                  ? "assignment"
                  : "assignments"}
              </span>
            </div>
          </div>

          {loading ? (
            <p>Loading deliveries...</p>
          ) : error ? (
            <p role="alert">{error}</p>
          ) : filteredAssignments.length === 0 ? (
            <p style={{ padding: "12px" }}>
              {assignments.length === 0
                ? "No delivery assignments available."
                : "No deliveries found for this status."}
            </p>
          ) : (
            <div
              style={{
                width: "100%",
                maxWidth: "100%",
                overflowX: "auto",
                WebkitOverflowScrolling: "touch",
              }}
            >
              <table
                style={{
                  width: "100%",
                  minWidth: "950px",
                  borderCollapse: "collapse",
                  textAlign: "left",
                }}
              >
                <thead>
                  <tr>
                    <th style={{ padding: "12px" }}>Assignment</th>
                    <th style={{ padding: "12px" }}>Donation ID</th>
                    <th style={{ padding: "12px" }}>Receiver ID</th>
                    <th style={{ padding: "12px" }}>Volunteer ID</th>
                    <th style={{ padding: "12px" }}>Pickup Time</th>
                    <th style={{ padding: "12px" }}>Delivery Time</th>
                    <th style={{ padding: "12px" }}>Status</th>
                  </tr>
                </thead>

                <tbody>
                  {filteredAssignments.map((assignment) => (
                    <tr key={assignment.id}>
                      <td style={{ padding: "12px" }}>
                        {assignment.id}
                      </td>

                      <td style={{ padding: "12px" }}>
                        {assignment.donation_id ?? "—"}
                      </td>

                      <td style={{ padding: "12px" }}>
                        {assignment.receiver_id ?? "—"}
                      </td>

                      <td style={{ padding: "12px" }}>
                        {assignment.volunteer_id ?? "—"}
                      </td>

                      <td
                        style={{
                          padding: "12px",
                          whiteSpace: "nowrap",
                        }}
                      >
                        {formatDate(assignment.pickup_time)}
                      </td>

                      <td
                        style={{
                          padding: "12px",
                          whiteSpace: "nowrap",
                        }}
                      >
                        {formatDate(assignment.delivery_time)}
                      </td>

                      <td
                        style={{
                          padding: "12px",
                          whiteSpace: "nowrap",
                        }}
                      >
                        <span style={getStatusStyle(assignment.status)}>
                          {(assignment.status || "pending").replaceAll(
                            "_",
                            " "
                          )}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default Deliveries;
