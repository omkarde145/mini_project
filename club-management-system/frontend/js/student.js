/**
 * Student Dashboard Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  if (!Auth.requireAuth(['student'])) return;

  const user = Auth.getUser();
  const studentNameEl = document.getElementById('student-name');
  if (studentNameEl) studentNameEl.textContent = user.full_name;

  // Stat elements
  const totalJoinedEl = document.getElementById('stat-joined');
  const totalPendingEl = document.getElementById('stat-pending');
  const totalEventsEl = document.getElementById('stat-events');

  // Containers
  const membershipsTableBody = document.getElementById('memberships-tbody');
  const announcementsFeed = document.getElementById('student-announcements-feed');
  const upcomingEventsContainer = document.getElementById('student-events-container');

  // Load Memberships
  async function loadMemberships() {
    try {
      const data = await apiRequest('/student/memberships');
      if (data.success) {
        const memberships = data.memberships;
        const approvedCount = memberships.filter(m => m.status === 'approved').length;
        const pendingCount = memberships.filter(m => m.status === 'pending').length;

        if (totalJoinedEl) totalJoinedEl.textContent = approvedCount;
        if (totalPendingEl) totalPendingEl.textContent = pendingCount;

        if (!membershipsTableBody) return;

        if (memberships.length === 0) {
          membershipsTableBody.innerHTML = `
            <tr>
              <td colspan="5" style="text-align: center; padding: 2rem;">
                No memberships yet. <a href="../index.html">Browse and join clubs now!</a>
              </td>
            </tr>
          `;
          return;
        }

        membershipsTableBody.innerHTML = memberships.map(mem => {
          let badgeClass = 'badge-pending';
          if (mem.status === 'approved') badgeClass = 'badge-approved';
          if (mem.status === 'rejected') badgeClass = 'badge-rejected';

          return `
            <tr>
              <td>
                <strong>${mem.club_name}</strong>
              </td>
              <td><span class="badge badge-category">${mem.club_category}</span></td>
              <td><span class="badge ${badgeClass}">${mem.status}</span></td>
              <td>${formatDate(mem.applied_at)}</td>
              <td>
                <div style="display: flex; gap: 0.5rem;">
                  <a href="club-details.html?id=${mem.club_id}" class="btn btn-outline btn-sm">View Club</a>
                  <button class="btn btn-secondary btn-sm" onclick="handleCancelMembership(${mem.club_id}, '${mem.status}')">
                    ${mem.status === 'approved' ? 'Leave' : 'Cancel'}
                  </button>
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

  // Load Feed (Announcements & Events)
  async function loadFeed() {
    try {
      const data = await apiRequest('/student/feed');
      if (data.success) {
        // Render Announcements
        if (announcementsFeed) {
          if (!data.announcements || data.announcements.length === 0) {
            announcementsFeed.innerHTML = `
              <div class="empty-state">
                <p>No club announcements yet. Join clubs to get real-time updates!</p>
              </div>
            `;
          } else {
            announcementsFeed.innerHTML = data.announcements.map(ann => `
              <div class="item-card">
                <div class="item-details">
                  <div class="item-meta">
                    <span class="badge badge-category">${ann.club_name}</span>
                    <span>🕒 ${formatDateTime(ann.posted_at)}</span>
                  </div>
                  <h4 class="item-title">${ann.title}</h4>
                  <p class="item-content">${ann.content}</p>
                </div>
              </div>
            `).join('');
          }
        }

        // Render Events
        if (upcomingEventsContainer) {
          const events = data.upcoming_events || [];
          if (totalEventsEl) totalEventsEl.textContent = events.length;

          if (events.length === 0) {
            upcomingEventsContainer.innerHTML = `
              <div class="empty-state">
                <p>No upcoming events for your clubs at this time.</p>
              </div>
            `;
          } else {
            upcomingEventsContainer.innerHTML = events.map(evt => `
              <div class="item-card">
                <div class="item-date-badge">
                  <div class="day">${getDayNumber(evt.event_date)}</div>
                  <div class="month">${getMonthShort(evt.event_date)}</div>
                </div>
                <div class="item-details">
                  <h4 class="item-title">${evt.title}</h4>
                  <div class="item-meta">
                    <span class="badge badge-category">${evt.club_name}</span>
                    <span>📍 ${evt.location}</span>
                    <span>⏰ ${formatDateTime(evt.event_date)}</span>
                  </div>
                  <p class="item-content">${evt.description}</p>
                </div>
              </div>
            `).join('');
          }
        }
      }
    } catch (err) {
      console.warn('Could not load student feed:', err);
    }
  }

  // Global handler for leave/cancel
  window.handleCancelMembership = async (clubId, currentStatus) => {
    const actionText = currentStatus === 'approved' ? 'leave this club' : 'cancel this membership request';
    if (!confirm(`Are you sure you want to ${actionText}?`)) return;

    try {
      const res = await apiRequest(`/student/memberships/${clubId}`, { method: 'DELETE' });
      if (res.success) {
        showToast(res.message, 'success');
        loadMemberships();
        loadFeed();
      }
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

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

  // Init
  loadMemberships();
  loadFeed();
});
