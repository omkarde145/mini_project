/**
 * Admin Oversight Dashboard Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  if (!Auth.requireAuth(['admin'])) return;

  // Stat Elements
  const statTotalClubs = document.getElementById('stat-total-clubs');
  const statPendingClubs = document.getElementById('stat-pending-clubs');
  const statStudents = document.getElementById('stat-students');
  const statCoordinators = document.getElementById('stat-coordinators');
  const statEvents = document.getElementById('stat-events');

  // Tables
  const pendingClubsTbody = document.getElementById('pending-clubs-tbody');
  const allClubsTbody = document.getElementById('all-clubs-tbody');
  const usersTbody = document.getElementById('users-tbody');
  const userSearchInput = document.getElementById('user-search');
  const userRoleFilter = document.getElementById('user-role-filter');

  let debounceUserSearch = null;

  // Load Platform Overview
  async function loadOverview() {
    try {
      const data = await apiRequest('/admin/overview');
      if (data.success) {
        const m = data.metrics;
        if (statTotalClubs) statTotalClubs.textContent = m.total_clubs;
        if (statPendingClubs) statPendingClubs.textContent = m.pending_clubs;
        if (statStudents) statStudents.textContent = m.total_students;
        if (statCoordinators) statCoordinators.textContent = m.total_coordinators;
        if (statEvents) statEvents.textContent = m.total_events;
      }
    } catch (err) {
      showToast('Failed to load overview: ' + err.message, 'error');
    }
  }

  // Load Pending Clubs for Approval
  async function loadPendingClubs() {
    if (!pendingClubsTbody) return;
    try {
      const data = await apiRequest('/admin/clubs?status=pending');
      if (data.success) {
        if (data.clubs.length === 0) {
          pendingClubsTbody.innerHTML = `
            <tr>
              <td colspan="5" style="text-align: center; padding: 2rem;">
                No pending club registrations to review.
              </td>
            </tr>
          `;
          return;
        }

        pendingClubsTbody.innerHTML = data.clubs.map(club => `
          <tr>
            <td><strong>${club.name}</strong></td>
            <td><span class="badge badge-category">${club.category}</span></td>
            <td>${club.coordinator_name || 'Unassigned'}</td>
            <td>${formatDate(club.created_at)}</td>
            <td>
              <div style="display: flex; gap: 0.5rem;">
                <button class="btn btn-success btn-sm" onclick="handleClubReview(${club.id}, 'approved')">Approve</button>
                <button class="btn btn-danger btn-sm" onclick="handleClubReview(${club.id}, 'rejected')">Reject</button>
              </div>
            </td>
          </tr>
        `).join('');
      }
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  // Load All Clubs Directory
  async function loadAllClubs() {
    if (!allClubsTbody) return;
    try {
      const data = await apiRequest('/admin/clubs');
      if (data.success) {
        allClubsTbody.innerHTML = data.clubs.map(club => {
          let badgeClass = 'badge-pending';
          if (club.status === 'approved') badgeClass = 'badge-approved';
          if (club.status === 'rejected') badgeClass = 'badge-rejected';

          return `
            <tr>
              <td><strong>${club.name}</strong></td>
              <td><span class="badge badge-category">${club.category}</span></td>
              <td>${club.coordinator_name || 'Unassigned'}</td>
              <td>👥 ${club.member_count || 0}</td>
              <td><span class="badge ${badgeClass}">${club.status}</span></td>
              <td>
                <div style="display: flex; gap: 0.5rem;">
                  ${club.status !== 'approved' ? `
                    <button class="btn btn-outline btn-sm" onclick="handleClubReview(${club.id}, 'approved')">Approve</button>
                  ` : ''}
                  ${club.status !== 'rejected' ? `
                    <button class="btn btn-secondary btn-sm" onclick="handleClubReview(${club.id}, 'rejected')">Reject</button>
                  ` : ''}
                </div>
              </td>
            </tr>
          `;
        }).join('');
      }
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  // Load System Users
  async function loadUsers() {
    if (!usersTbody) return;
    try {
      let endpoint = '/admin/users?';
      const role = userRoleFilter ? userRoleFilter.value : '';
      const search = userSearchInput ? userSearchInput.value.trim() : '';

      if (role) endpoint += `role=${encodeURIComponent(role)}&`;
      if (search) endpoint += `search=${encodeURIComponent(search)}&`;

      const data = await apiRequest(endpoint);
      if (data.success) {
        if (data.users.length === 0) {
          usersTbody.innerHTML = `
            <tr>
              <td colspan="6" style="text-align: center; padding: 2rem;">No users found.</td>
            </tr>
          `;
          return;
        }

        usersTbody.innerHTML = data.users.map(u => {
          const isActive = u.is_active === 1 || u.is_active === true;
          return `
            <tr>
              <td>
                <strong>${u.full_name}</strong>
                <div style="font-size: 0.75rem; color: var(--gray-500);">${u.email}</div>
              </td>
              <td>
                <select class="form-select" style="padding: 0.25rem 0.5rem; font-size: 0.8125rem; width: auto;" onchange="handleRoleChange(${u.id}, this.value)">
                  <option value="student" ${u.role === 'student' ? 'selected' : ''}>Student</option>
                  <option value="coordinator" ${u.role === 'coordinator' ? 'selected' : ''}>Coordinator</option>
                  <option value="admin" ${u.role === 'admin' ? 'selected' : ''}>Admin</option>
                </select>
              </td>
              <td>${u.department || 'N/A'}</td>
              <td>${u.student_id || 'N/A'}</td>
              <td>
                <span class="badge ${isActive ? 'badge-active' : 'badge-inactive'}">
                  ${isActive ? 'Active' : 'Deactivated'}
                </span>
              </td>
              <td>
                <button class="btn ${isActive ? 'btn-secondary' : 'btn-success'} btn-sm" onclick="handleToggleUserStatus(${u.id})">
                  ${isActive ? 'Deactivate' : 'Activate'}
                </button>
              </td>
            </tr>
          `;
        }).join('');
      }
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  // Load Coordinators for Create Club Modal dropdown
  async function loadCoordinatorsDropdown() {
    const select = document.getElementById('new-club-coordinator');
    if (!select) return;
    try {
      const data = await apiRequest('/admin/coordinators');
      if (data.success) {
        select.innerHTML = '<option value="">-- Select Coordinator (Optional) --</option>' +
          data.coordinators.map(c => `<option value="${c.id}">${c.full_name} (${c.email})</option>`).join('');
      }
    } catch (err) {
      console.warn('Could not load coordinators dropdown:', err);
    }
  }

  // Club Review Action
  window.handleClubReview = async (clubId, newStatus) => {
    try {
      const res = await apiRequest(`/admin/clubs/${clubId}/status`, {
        method: 'POST',
        body: JSON.stringify({ status: newStatus })
      });
      if (res.success) {
        showToast(res.message, 'success');
        loadOverview();
        loadPendingClubs();
        loadAllClubs();
      }
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  // Toggle User Status
  window.handleToggleUserStatus = async (userId) => {
    try {
      const res = await apiRequest(`/admin/users/${userId}/toggle-status`, { method: 'POST' });
      if (res.success) {
        showToast(res.message, 'success');
        loadOverview();
        loadUsers();
      }
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  // Change User Role
  window.handleRoleChange = async (userId, newRole) => {
    try {
      const res = await apiRequest(`/admin/users/${userId}/role`, {
        method: 'POST',
        body: JSON.stringify({ role: newRole })
      });
      if (res.success) {
        showToast(res.message, 'success');
        loadOverview();
        loadUsers();
      }
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  // Create Club Form
  const createClubForm = document.getElementById('create-club-form');
  if (createClubForm) {
    createClubForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const payload = {
        name: document.getElementById('new-club-name').value,
        category: document.getElementById('new-club-category').value,
        description: document.getElementById('new-club-desc').value,
        banner_url: document.getElementById('new-club-banner').value,
        coordinator_id: document.getElementById('new-club-coordinator').value || null,
        status: 'approved'
      };

      try {
        const res = await apiRequest('/admin/clubs', {
          method: 'POST',
          body: JSON.stringify(payload)
        });
        if (res.success) {
          showToast('Club registered and activated successfully!', 'success');
          closeModal('create-club-modal');
          createClubForm.reset();
          loadOverview();
          loadAllClubs();
        }
      } catch (err) {
        showToast(err.message, 'error');
      }
    });
  }

  // Filter Listeners for Users
  if (userRoleFilter) {
    userRoleFilter.addEventListener('change', loadUsers);
  }
  if (userSearchInput) {
    userSearchInput.addEventListener('input', () => {
      clearTimeout(debounceUserSearch);
      debounceUserSearch = setTimeout(loadUsers, 300);
    });
  }

  // Tab switching
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

      e.target.classList.add('active');
      const targetPane = document.getElementById(e.target.dataset.target);
      if (targetPane) targetPane.classList.add('active');
    });
  });

  // Modal helper functions
  window.openModal = (modalId) => {
    const el = document.getElementById(modalId);
    if (el) el.classList.add('show');
  };

  window.closeModal = (modalId) => {
    const el = document.getElementById(modalId);
    if (el) el.classList.remove('show');
  };

  // Initialize
  loadOverview();
  loadPendingClubs();
  loadAllClubs();
  loadUsers();
  loadCoordinatorsDropdown();
});
