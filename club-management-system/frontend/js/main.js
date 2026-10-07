/**
 * Landing Page - Club Exploration, Filters & Search
 */

document.addEventListener('DOMContentLoaded', () => {
  let activeCategory = 'all';
  let searchQuery = '';
  let debounceTimer = null;

  const searchInput = document.getElementById('search-input');
  const searchBtn = document.getElementById('search-btn');
  const categoryFilters = document.getElementById('category-filters');
  const clubGrid = document.getElementById('club-grid');
  const clubCountBadge = document.getElementById('club-count-badge');

  // Load Categories
  async function loadCategories() {
    try {
      const data = await apiRequest('/student/categories');
      if (data.success && categoryFilters) {
        let chipsHtml = `<button class="filter-chip active" data-category="all">All Clubs</button>`;
        data.categories.forEach(cat => {
          chipsHtml += `<button class="filter-chip" data-category="${cat}">${cat}</button>`;
        });
        categoryFilters.innerHTML = chipsHtml;

        // Attach click listeners to chips
        categoryFilters.querySelectorAll('.filter-chip').forEach(btn => {
          btn.addEventListener('click', (e) => {
            categoryFilters.querySelectorAll('.filter-chip').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            activeCategory = e.target.getAttribute('data-category');
            loadClubs();
          });
        });
      }
    } catch (err) {
      console.warn('Could not load categories:', err);
    }
  }

  // Load Clubs
  async function loadClubs() {
    if (!clubGrid) return;
    clubGrid.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 3rem;">
        <p>Loading campus clubs...</p>
      </div>
    `;

    try {
      let endpoint = `/student/clubs?`;
      if (activeCategory && activeCategory !== 'all') {
        endpoint += `category=${encodeURIComponent(activeCategory)}&`;
      }
      if (searchQuery) {
        endpoint += `search=${encodeURIComponent(searchQuery)}&`;
      }

      const data = await apiRequest(endpoint);
      if (data.success) {
        if (clubCountBadge) {
          clubCountBadge.textContent = `${data.count} Available`;
        }

        if (data.clubs.length === 0) {
          clubGrid.innerHTML = `
            <div class="empty-state" style="grid-column: 1/-1;">
              <div class="empty-state-icon">🔍</div>
              <h3>No clubs found</h3>
              <p>Try searching for a different keyword or category.</p>
            </div>
          `;
          return;
        }

        const isPagesDir = window.location.pathname.includes('/pages/');
        const detailsUrlPrefix = isPagesDir ? 'club-details.html' : 'pages/club-details.html';

        clubGrid.innerHTML = data.clubs.map(club => {
          const banner = club.banner_url || 'https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=800&auto=format&fit=crop&q=80';
          return `
            <div class="card club-card">
              <div class="club-card-banner">
                <img src="${banner}" alt="${club.name}" onerror="this.src='https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=800&auto=format&fit=crop&q=80'">
                <span class="badge badge-category club-card-category">${club.category}</span>
              </div>
              <div class="club-card-content">
                <h3 class="club-card-title">${club.name}</h3>
                <p class="club-card-desc">${club.description}</p>
                <div class="club-card-footer">
                  <span>👥 ${club.member_count || 0} Members</span>
                  <span>📅 ${club.event_count || 0} Events</span>
                </div>
                <div style="margin-top: 1rem;">
                  <a href="${detailsUrlPrefix}?id=${club.id}" class="btn btn-outline btn-sm" style="width: 100%;">
                    View Details & Join &rarr;
                  </a>
                </div>
              </div>
            </div>
          `;
        }).join('');
      }
    } catch (err) {
      clubGrid.innerHTML = `
        <div class="empty-state" style="grid-column: 1/-1;">
          <div class="empty-state-icon">⚠️</div>
          <h3>Failed to load clubs</h3>
          <p>${err.message}</p>
        </div>
      `;
    }
  }

  // Search input listeners
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        searchQuery = e.target.value.trim();
        loadClubs();
      }, 300);
    });
  }

  if (searchBtn) {
    searchBtn.addEventListener('click', () => {
      searchQuery = searchInput.value.trim();
      loadClubs();
    });
  }

  // Initialize
  loadCategories();
  loadClubs();
});
