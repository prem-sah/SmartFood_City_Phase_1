function Sidebar() {
  return (
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
  );
}

export default Sidebar;
