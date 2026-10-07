# Campus Club Management System

A complete, fully functional, and reproducible full-stack web application for university and collegiate club management. Built with Vanilla HTML5/CSS3/JavaScript (ES6+ Fetch API), Python Flask, and a relational MySQL database with strict Role-Based Access Control (RBAC).

---

## 🚀 Features by Role

### 1. 🎓 Student
- **Club Discovery**: Search clubs by keyword, filter by categories (Technology, Arts & Culture, Music, Environment, Academic).
- **Club Details**: View club profile, lead coordinator contact, announcements, and upcoming/past events.
- **Membership Applications**: Send 1-click join requests with real-time status tracking (`Pending`, `Approved`, `Rejected`), with option to cancel or re-apply.
- **Student Dashboard**: Personalized hub with active club memberships, combined activity announcements feed, and upcoming event schedules.

### 2. ⚡ Club Coordinator
- **Club Profile Management**: Update club details, description, category, and banner imagery.
- **Membership Request Review**: Dedicated inbox to review student join requests with 1-click **Approve** or **Reject**.
- **Member Roster Management**: View all active members with student IDs and department info, with the ability to remove members.
- **Events Management**: Full CRUD (Create, Edit, Delete) for club events and workshops with dates and locations.
- **Announcements Management**: Full CRUD for club broadcasts and news updates.

### 3. 🛡️ Administrator
- **Platform Analytics**: High-level metrics for total clubs, pending clubs, students, coordinators, and active events.
- **Club Verification**: Review and approve or reject newly registered clubs and coordinator assignments.
- **Direct Club Creation**: Register new campus clubs and assign lead coordinators directly.
- **User Administration**: Comprehensive user directory with real-time search, role filtering, one-click Account Activation/Deactivation, and role reassignment (`student` ↔ `coordinator` ↔ `admin`).

---

## 📂 Project Directory Structure

```
club-management-system/
├── README.md                   # Complete documentation & setup instructions
├── database/
│   ├── schema.sql              # MySQL DDL (tables, foreign keys, constraints & indexes)
│   └── seed.sql                # Pre-populated test accounts and sample campus clubs
├── backend/
│   ├── app.py                  # Flask entry point, blueprint registration & static serving
│   ├── config.py               # Database URI, secret keys & CORS settings
│   ├── init_db.py              # CLI utility to initialize and seed database
│   ├── test_api.py             # Automated test suite for backend API endpoints
│   ├── requirements.txt        # Python dependencies
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # User model (Student, Coordinator, Admin)
│   │   ├── club.py             # Club model & category handling
│   │   ├── membership.py       # Membership request & status model
│   │   ├── event.py            # Events model (upcoming & past events)
│   │   └── announcement.py     # Announcements model
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py      # Register, login, session /me validation
│   │   ├── student_routes.py   # Club browsing, join requests, my memberships, feed
│   │   ├── coordinator_routes.py # Request approvals, member roster, event/announcement CRUD
│   │   └── admin_routes.py     # Platform stats, club approval, user management
│   └── utils/
│       ├── db.py               # PyMySQL connection handler with DictCursor & query helper
│       └── decorators.py       # JWT generator, @login_required, @role_required
└── frontend/
    ├── index.html              # Landing page with public club discovery & live search
    ├── login.html              # Authentication page (Login / Register with demo accounts)
    ├── css/
    │   ├── style.css           # Global typography, color tokens, badges & modals
    │   ├── navbar.css          # Navigation bar styles with dynamic auth state
    │   └── dashboard.css       # Layout styles for dashboards, cards & stat counters
    ├── js/
    │   ├── api.js              # Centralized Fetch API client with toast notifications
    │   ├── auth.js             # Client session, role management & dynamic navbar
    │   ├── main.js             # Landing page club exploration, filters & search
    │   ├── student.js          # Student dashboard logic (memberships, feed, calendar)
    │   ├── coordinator.js      # Coordinator actions (approve/reject, post events)
    │   └── admin.js            # Admin oversight dashboard logic
    └── pages/
        ├── student-dashboard.html
        ├── coordinator-dashboard.html
        ├── admin-dashboard.html
        └── club-details.html
```

---

## 🔑 Pre-Configured Test Accounts

All pre-populated seed accounts use the password: **`password123`**

| Role | Name | Email | Password | Affiliation / Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Admin** | System Administrator | `admin@campus.edu` | `password123` | Platform oversight & user management |
| **Coordinator** | Alex Rivera | `coding.lead@campus.edu` | `password123` | Lead of **Coding Club** |
| **Coordinator** | Elena Rostova | `robotics.lead@campus.edu` | `password123` | Lead of **Robotics Society** |
| **Coordinator** | Marcus Chen | `arts.lead@campus.edu` | `password123` | Lead of **Fine Arts Guild** |
| **Student** | Sarah Jenkins | `student1@campus.edu` | `password123` | Active member in Coding Club, pending in Robotics |
| **Student** | Liam O'Connor | `student2@campus.edu` | `password123` | Active in Coding Club, pending in Fine Arts |
| **Student** | Aaliyah Khan | `student3@campus.edu` | `password123` | Active in Robotics, pending in Coding Club |

*(On `login.html`, click any of the demo account pills to instantly autofill the credentials!)*

---

## ⚡ 1-Click Quick Launch (Windows)

Simply double-click the **[`start_app.bat`](file:///d:/mini%20project/start_app.bat)** batch file located in the project folder!
- It verifies Python.
- Auto-initializes database & seed data if first launch.
- Starts the Flask application server on port 5000.
- Automatically launches your default web browser to `http://127.0.0.1:5000`.

---

## ⚙️ Step-by-Step Installation & Setup

### Prerequisites
- Python 3.9+
- MySQL Server 5.7+ / 8.0+ (via MySQL Server, XAMPP, WampServer, or Docker)
  *(Note: The backend also contains automatic local fallback if MySQL is not running on localhost)*

---

### Step 1: Database Setup (MySQL)

#### Option A: Using MySQL Command Line
1. Open your terminal or MySQL command line client:
```bash
mysql -u root -p
```
2. Import the schema and seed scripts:
```sql
source database/schema.sql;
source database/seed.sql;
```

#### Option B: Using the Included Python Initializer
You can also run the initialization script directly from the backend directory:
```bash
cd backend
python init_db.py --mysql
```

---

### Step 2: Backend Setup (Python Flask)

1. Open a terminal in the `backend/` directory:
```bash
cd backend
```

2. (Optional but recommended) Create and activate a Python virtual environment:
- **Windows (PowerShell/CMD):**
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

3. Install the required Python packages:
```bash
pip install -r requirements.txt
```

4. Configure environment variables (optional):
Create a `.env` file in the `backend/` directory if your MySQL credentials differ from defaults:
```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=club_management_db
SECRET_KEY=your_secret_key
PORT=5000
```

5. Run automated tests to verify the setup:
```bash
python test_api.py
```
*(All 7 tests will execute and confirm health, authentication, roles, and endpoints).*

6. Start the Flask server:
```bash
python app.py
```
The server will start listening at:
👉 **`http://127.0.0.1:5000`**

---

### Step 3: Running the Frontend

You can run the frontend in any of the following ways:

#### Option A: Directly Through Flask (Zero Extra Config)
Since `backend/app.py` automatically serves the static frontend, simply open your browser to:
👉 **`http://127.0.0.1:5000`**

#### Option B: Using VS Code Live Server
1. Open the project in VS Code.
2. Right-click `frontend/index.html` and choose **"Open with Live Server"**.
3. The frontend will communicate seamlessly with `http://127.0.0.1:5000/api` via CORS.

#### Option C: Using Python's Built-in HTTP Server
From the project root:
```bash
cd frontend
python -m http.server 3000
```
Then visit **`http://localhost:3000`**.

---

## 📡 REST API Reference

### Authentication (`/api/auth`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Register student or coordinator | No |
| `POST` | `/api/auth/login` | Login and receive JWT token | No |
| `GET` | `/api/auth/me` | Retrieve profile of authenticated user | Yes |
| `POST` | `/api/auth/logout` | Client logout confirmation | No |

### Student Endpoints (`/api/student`)
| Method | Endpoint | Description | Role Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/student/categories` | List distinct club categories | Public |
| `GET` | `/api/student/clubs` | Search & filter approved clubs | Public |
| `GET` | `/api/student/clubs/<id>` | Full club profile with events & announcements | Public / Authenticated |
| `POST` | `/api/student/clubs/<id>/join` | Apply to join a club | `student` |
| `GET` | `/api/student/memberships` | List my memberships with status | `student` |
| `DELETE` | `/api/student/memberships/<club_id>` | Cancel pending request or leave club | `student` |
| `GET` | `/api/student/feed` | Combined notifications and event feed | `student` |

### Coordinator Endpoints (`/api/coordinator`)
| Method | Endpoint | Description | Role Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/coordinator/club` | View assigned club profile & statistics | `coordinator` |
| `PUT` | `/api/coordinator/club` | Update club name, description, banner | `coordinator` |
| `GET` | `/api/coordinator/requests` | List incoming membership applications | `coordinator` |
| `POST` | `/api/coordinator/requests/<id>/action` | Approve or Reject application | `coordinator` |
| `GET` | `/api/coordinator/members` | View approved member roster | `coordinator` |
| `DELETE` | `/api/coordinator/members/<user_id>` | Remove member from club roster | `coordinator` |
| `GET` | `/api/coordinator/events` | List all club events | `coordinator` |
| `POST` | `/api/coordinator/events` | Create new club event | `coordinator` |
| `PUT` | `/api/coordinator/events/<id>` | Update event details | `coordinator` |
| `DELETE` | `/api/coordinator/events/<id>` | Delete event | `coordinator` |
| `GET` | `/api/coordinator/announcements` | List club announcements | `coordinator` |
| `POST` | `/api/coordinator/announcements` | Post new announcement | `coordinator` |
| `PUT` | `/api/coordinator/announcements/<id>` | Edit announcement | `coordinator` |
| `DELETE` | `/api/coordinator/announcements/<id>` | Delete announcement | `coordinator` |

### Admin Endpoints (`/api/admin`)
| Method | Endpoint | Description | Role Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/admin/overview` | Platform analytics & counts | `admin` |
| `GET` | `/api/admin/clubs` | List all clubs across statuses | `admin` |
| `POST` | `/api/admin/clubs/<id>/status` | Approve or Reject club registration | `admin` |
| `POST` | `/api/admin/clubs` | Create club directly and assign lead | `admin` |
| `GET` | `/api/admin/users` | List system users with search/role filters | `admin` |
| `POST` | `/api/admin/users/<id>/toggle-status`| Toggle user active/deactivated status | `admin` |
| `POST` | `/api/admin/users/<id>/role` | Reassign user role | `admin` |
| `GET` | `/api/admin/coordinators` | List coordinators available for assignment | `admin` |

---

## 🔒 Security Implementations
- **Password Protection**: Passwords securely hashed using standard `scrypt` via Werkzeug. Plaintext passwords are never saved.
- **Stateless Authentication**: JWT tokens with 24-hour expiration (`exp`), subject claims, and secret signatures.
- **RBAC Decorators**: `@login_required` and `@role_required` strictly gate administrative and coordinator resources.
- **SQL Injection Prevention**: All queries utilize parameterized SQL placeholders (`%s`) handled directly by the database driver.
- **Deactivated Account Gating**: Suspended user accounts are immediately barred from generating tokens or accessing endpoints even with existing sessions.
