/**
 * Coordinator Dashboard Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  if (!Auth.requireAuth(['coordinator'])) return;

  let currentClub = null;

  // Stat Elements
  const clubNameEl = document.getElementById('coordinator-club-name');
  const clubCategoryEl = document.getElementById('coordinator-club-category');
  const statMembersEl = document.getElementById('stat-members');
  const statPendingEl = document.getElementById('stat-pending');
  const statEventsEl = document.getElementById('stat-events');
  const statAnnouncementsEl = document.getElementById('stat-announcements');

  // Containers
  const requestsTbody = document.getElementById('requests-tbody');
  const membersTbody = document.getElementById('members-tbody');
  const eventsListEl = document.getElementById('coordinator-events-list');
  const announcementsListEl = document.getElementById('coordinator-announcements-list');

  // Load Coordinator Club Info
  async function loadClubDetails() {
    try {
      const data = await apiRequest('/coordinator/club');
      if (data.success) {
        currentClub = data.club;
        if (clubNameEl) clubNameEl.textContent = currentClub.name;
        if (clubCategoryEl) clubCategoryEl.textContent = currentClub.category;

        if (statMembersEl) statMembersEl.textContent = currentClub.member_count || 0;
        if (statPendingEl) statPendingEl.textContent = currentClub.pending_requests_count || 0;
        if (statEventsEl) statEventsEl.textContent = currentClub.event_count || 0;
        if (statAnnouncementsEl) statAnnouncementsEl.textContent = currentClub.announcement_count || 0;

        // Prepopulate edit modal inputs
        document.getElementById('edit-club-name').value = currentClub.name || '';
        document.getElementById('edit-club-category').value = currentClub.category || '';
        document.getElementById('edit-club-banner').value = currentClub.banner_url || '';
        document.getElementById('edit-club-desc').value = currentClub.description || '';
      }
    } catch (err) {
      showToast('Failed to load club details: ' + err.message, 'error');
    }
  }

  // Load Pending Membership Requests
  async function loadPendingRequests() {
    if (!requestsTbody) return;
    try {
      const data = await apiRequest('/coordinator/requests');
      if (data.success) {
        if (data.requests.length === 0) {
          requestsTbody.innerHTML = `
            <tr>
              <td colspan="5" style="text-align: center; padding: 2rem;">
                No pending membership requests right now.
              </td>
            </tr>
          `;
          return;
        }

        requestsTbody.innerHTML = data.requests.map(req => `
          <tr>
            <td>
              <strong>${req.full_name}</strong>
              <div style="font-size: 0.75rem; color: var(--gray-500);">${req.student_id || 'ID N/A'}</div>
            </td>
            <td>${req.email}</td>
            <td>${req.department || 'N/A'}</td>
            <td>${formatDate(req.applied_at)}</td>
            <td>
              <div style="display: flex; gap: 0.5rem;">
                <button class="btn btn-success btn-sm" onclick="handleRequestAction(${req.membership_id}, 'approved')">
                  Approve
                </button>
                <button class="btn btn-danger btn-sm" onclick="handleRequestAction(${req.membership_id}, 'rejected')">
                  Reject
                </button>
              </div>
            </td>
          </tr>
        `).join('');
      }
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  // Load Member Roster
  async function loadMemberRoster() {
    if (!membersTbody) return;
    try {
      const data = await apiRequest('/coordinator/members');
      if (data.success) {
        if (data.members.length === 0) {
          membersTbody.innerHTML = `
            <tr>
              <td colspan="5" style="text-align: center; padding: 2rem;">
                No active members found. Approve pending requests to grow your club!
              </td>
            </tr>
          `;
          return;
        }

        membersTbody.innerHTML = data.members.map(member => `
          <tr>
            <td>
              <strong>${member.full_name}</strong>
              <div style="font-size: 0.75rem; color: var(--gray-500);">${member.student_id || 'ID N/A'}</div>
            </td>
            <td>${member.email}</td>
            <td>${member.department || 'N/A'}</td>
            <td>${formatDate(member.applied_at)}</td>
            <td>
              <button class="btn btn-secondary btn-sm" onclick="handleRemoveMember(${member.user_id}, '${member.full_name}')">
                Remove
              </button>
            </td>
          </tr>
        `).join('');
      }
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  // Load Events
  async function loadEvents() {
    if (!eventsListEl) return;
    try {
      const data = await apiRequest('/coordinator/events');
      if (data.success) {
        if (data.events.length === 0) {
          eventsListEl.innerHTML = `
            <div class="empty-state">
              <p>No events scheduled. Create your first club event!</p>
            </div>
          `;
          return;
        }

        eventsListEl.innerHTML = data.events.map(evt => `
          <div class="item-card">
            <div class="item-date-badge">
              <div class="day">${getDayNumber(evt.event_date)}</div>
              <div class="month">${getMonthShort(evt.event_date)}</div>
            </div>
            <div class="item-details">
              <h4 class="item-title">${evt.title}</h4>
              <div class="item-meta">
                <span>📍 ${evt.location}</span>
                <span>⏰ ${formatDateTime(evt.event_date)}</span>
              </div>
              <p class="item-content">${evt.description}</p>
            </div>
            <div style="display: flex; gap: 0.5rem; flex-direction: column;">
              <button class="btn btn-outline btn-sm" onclick="openEditEventModal(${JSON.stringify(evt).replace(/"/g, '&quot;')})">Edit</button>
              <button class="btn btn-danger btn-sm" onclick="handleDeleteEvent(${evt.id})">Delete</button>
            </div>
          </div>
        `).join('');
      }
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  // Load Announcements
  async function loadAnnouncements() {
    if (!announcementsListEl) return;
    try {
      const data = await apiRequest('/coordinator/announcements');
      if (data.success) {
        if (data.announcements.length === 0) {
          announcementsListEl.innerHTML = `
            <div class="empty-state">
              <p>No announcements posted yet.</p>
            </div>
          `;
          return;
        }

        announcementsListEl.innerHTML = data.announcements.map(ann => `
          <div class="item-card">
            <div class="item-details">
              <div class="item-meta">
                <span>🕒 Posted: ${formatDateTime(ann.posted_at)}</span>
              </div>
              <h4 class="item-title">${ann.title}</h4>
              <p class="item-content">${ann.content}</p>
            </div>
            <div style="display: flex; gap: 0.5rem; flex-direction: column;">
              <button class="btn btn-outline btn-sm" onclick="openEditAnnouncementModal(${JSON.stringify(ann).replace(/"/g, '&quot;')})">Edit</button>
              <button class="btn btn-danger btn-sm" onclick="handleDeleteAnnouncement(${ann.id})">Delete</button>
            </div>
          </div>
        `).join('');
      }
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  // Action Request (Approve / Reject)
  window.handleRequestAction = async (membershipId, action) => {
    try {
      const res = await apiRequest(`/coordinator/requests/${membershipId}/action`, {
        method: 'POST',
        body: JSON.stringify({ action })
      });
      if (res.success) {
        showToast(res.message, 'success');
        loadClubDetails();
        loadPendingRequests();
        loadMemberRoster();
      }
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  // Remove Member
  window.handleRemoveMember = async (studentId, studentName) => {
    if (!confirm(`Are you sure you want to remove ${studentName} from the club?`)) return;
    try {
      const res = await apiRequest(`/coordinator/members/${studentId}`, { method: 'DELETE' });
      if (res.success) {
        showToast(res.message, 'success');
        loadClubDetails();
        loadMemberRoster();
      }
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  // Delete Event
  window.handleDeleteEvent = async (eventId) => {
    if (!confirm('Are you sure you want to delete this event?')) return;
    try {
      const res = await apiRequest(`/coordinator/events/${eventId}`, { method: 'DELETE' });
      if (res.success) {
        showToast(res.message, 'success');
        loadClubDetails();
        loadEvents();
      }
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  // Delete Announcement
  window.handleDeleteAnnouncement = async (annId) => {
    if (!confirm('Are you sure you want to delete this announcement?')) return;
    try {
      const res = await apiRequest(`/coordinator/announcements/${annId}`, { method: 'DELETE' });
      if (res.success) {
        showToast(res.message, 'success');
        loadClubDetails();
        loadAnnouncements();
      }
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  // Edit Club Profile Form
  const editClubForm = document.getElementById('edit-club-form');
  if (editClubForm) {
    editClubForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const payload = {
        name: document.getElementById('edit-club-name').value,
        category: document.getElementById('edit-club-category').value,
        banner_url: document.getElementById('edit-club-banner').value,
        description: document.getElementById('edit-club-desc').value
      };

      try {
        const res = await apiRequest('/coordinator/club', {
          method: 'PUT',
          body: JSON.stringify(payload)
        });
        if (res.success) {
          showToast('Club profile updated successfully!', 'success');
          closeModal('edit-club-modal');
          loadClubDetails();
        }
      } catch (err) {
        showToast(err.message, 'error');
      }
    });
  }

  // Create / Edit Event Form
  const eventForm = document.getElementById('event-form');
  if (eventForm) {
    eventForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const eventId = document.getElementById('event-id').value;
      const payload = {
        title: document.getElementById('event-title').value,
        location: document.getElementById('event-location').value,
        event_date: document.getElementById('event-date').value,
        description: document.getElementById('event-desc').value
      };

      try {
        const url = eventId ? `/coordinator/events/${eventId}` : '/coordinator/events';
        const method = eventId ? 'PUT' : 'POST';
        const res = await apiRequest(url, { method, body: JSON.stringify(payload) });

        if (res.success) {
          showToast(res.message, 'success');
          closeModal('event-modal');
          loadClubDetails();
          loadEvents();
        }
      } catch (err) {
        showToast(err.message, 'error');
      }
    });
  }

  // Create / Edit Announcement Form
  const annForm = document.getElementById('announcement-form');
  if (annForm) {
    annForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const annId = document.getElementById('announcement-id').value;
      const payload = {
        title: document.getElementById('announcement-title').value,
        content: document.getElementById('announcement-content').value
      };

      try {
        const url = annId ? `/coordinator/announcements/${annId}` : '/coordinator/announcements';
        const method = annId ? 'PUT' : 'POST';
        const res = await apiRequest(url, { method, body: JSON.stringify(payload) });

        if (res.success) {
          showToast(res.message, 'success');
          closeModal('announcement-modal');
          loadClubDetails();
          loadAnnouncements();
        }
      } catch (err) {
        showToast(err.message, 'error');
      }
    });
  }

  // Modal openers
  window.openEditEventModal = (evt) => {
    document.getElementById('event-modal-title').textContent = evt ? 'Edit Event' : 'Create New Event';
    document.getElementById('event-id').value = evt ? evt.id : '';
    document.getElementById('event-title').value = evt ? evt.title : '';
    document.getElementById('event-location').value = evt ? evt.location : '';
    // Format datetime-local string (YYYY-MM-DDTHH:MM)
    if (evt && evt.event_date) {
      const d = new Date(evt.event_date);
      const iso = new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
      document.getElementById('event-date').value = iso;
    } else {
      document.getElementById('event-date').value = '';
    }
    document.getElementById('event-desc').value = evt ? evt.description : '';
    openModal('event-modal');
  };

  window.openEditAnnouncementModal = (ann) => {
    document.getElementById('announcement-modal-title').textContent = ann ? 'Edit Announcement' : 'Post Announcement';
    document.getElementById('announcement-id').value = ann ? ann.id : '';
    document.getElementById('announcement-title').value = ann ? ann.title : '';
    document.getElementById('announcement-content').value = ann ? ann.content : '';
    openModal('announcement-modal');
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
  loadClubDetails();
  loadPendingRequests();
  loadMemberRoster();
  loadEvents();
  loadAnnouncements();
});
