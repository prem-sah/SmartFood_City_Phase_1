const API_BASE_URL = "http://127.0.0.1:8000";

export async function getDashboardSummary() {
  const response = await fetch(
    `${API_BASE_URL}/dashboard/summary`
  );

  if (!response.ok) {
    throw new Error("Failed to load dashboard summary");
  }

  return response.json();
}

export async function getDashboardDonations() {
  const response = await fetch(
    `${API_BASE_URL}/dashboard/donations`
  );

  if (!response.ok) {
    throw new Error("Failed to load dashboard donations");
  }

  return response.json();
}

export async function getDonors() {
  const response = await fetch(
    `${API_BASE_URL}/donors/`
  );

  if (!response.ok) {
    throw new Error("Failed to load donors");
  }

  return response.json();
}
