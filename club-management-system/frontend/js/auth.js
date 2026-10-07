/**
 * Client-Side Session & Role Management
 */

const Auth = {
  getToken() {
    return localStorage.getItem('auth_token');
  },

  getUser() {
    const raw = localStorage.getItem('user_data');
    try {
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  },

  getClub() {
    const raw = localStorage.getItem('club_data');
    try {
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  },

  setSession(token, user, club = null) {
    localStorage.setItem('auth_token', token);
    localStorage.setItem('user_data', JSON.stringify(user));
    if (club) {
      localStorage.setItem('club_data', JSON.stringify(club));
    } else {
      localStorage.removeItem('club_data');
    }
  },

  clearSession() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_data');
    localStorage.removeItem('club_data');
  },

  isAuthenticated() {
    return !!this.getToken();
  },

  getDashboardUrl(role) {
    const isPagesDir = window.location.pathname.includes('/pages/');
    const prefix = isPagesDir ? '' : 'pages/';
    switch (role) {
      case 'admin':
        return `${prefix}admin-dashboard.html`;
      case 'coordinator':
        return `${prefix}coordinator-dashboard.html`;
      case 'student':
      default:
        return `${prefix}student-dashboard.html`;
    }
  },

  requireAuth(allowedRoles = []) {
    if (!this.isAuthenticated()) {
      const isPagesDir = window.location.pathname.includes('/pages/');
      const loginUrl = isPagesDir ? '../login.html' : 'login.html';
      window.location.href = loginUrl;
      return false;
    }

    const user = this.getUser();
    if (allowedRoles.length > 0 && (!user || !allowedRoles.includes(user.role))) {
      showToast('Unauthorized access. Redirecting...', 'error');
      setTimeout(() => {
        window.location.href = this.getDashboardUrl(user ? user.role : 'student');
      }, 1000);
      return false;
    }

    return true;
  },

  logout() {
    this.clearSession();
    showToast('Logged out successfully', 'info');
    setTimeout(() => {
      const isPagesDir = window.location.pathname.includes('/pages/');
      window.location.href = isPagesDir ? '../index.html' : 'index.html';
    }, 500);
  },

  renderNavbar() {
    const navContainer = document.getElementById('navbar-auth-actions');
    if (!navContainer) return;

    const isPagesDir = window.location.pathname.includes('/pages/');
    const homeUrl = isPagesDir ? '../index.html' : 'index.html';
    const loginUrl = isPagesDir ? '../login.html' : 'login.html';

    if (this.isAuthenticated()) {
      const user = this.getUser();
      const dashboardUrl = this.getDashboardUrl(user.role);
      const initial = user.full_name ? user.full_name.charAt(0) : 'U';

      navContainer.innerHTML = `
        <div class="user-profile-badge">
          <div class="user-avatar">${initial}</div>
          <div class="user-info">
            <span class="user-name">${user.full_name}</span>
            <span class="user-role-label">${user.role}</span>
          </div>
        </div>
        <a href="${dashboardUrl}" class="btn btn-outline btn-sm">Dashboard</a>
        <button id="nav-logout-btn" class="btn btn-secondary btn-sm">Logout</button>
      `;

      const logoutBtn = document.getElementById('nav-logout-btn');
      if (logoutBtn) {
        logoutBtn.addEventListener('click', () => this.logout());
      }
    } else {
      navContainer.innerHTML = `
        <a href="${loginUrl}" class="btn btn-outline btn-sm">Sign In</a>
        <a href="${loginUrl}?tab=register" class="btn btn-primary btn-sm">Get Started</a>
      `;
    }
  }
};

// Auto-render navbar on page load
document.addEventListener('DOMContentLoaded', () => {
  Auth.renderNavbar();
});
