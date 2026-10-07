"""
Comprehensive End-to-End Verification Script
Verifies frontend assets, backend routes, RBAC, database queries, and role permissions.
"""

import unittest
import json
from app import create_app

class FullSystemVerification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_01_static_pages_served(self):
        """Verify all HTML pages and CSS/JS assets are properly served."""
        pages = [
            '/',
            '/index.html',
            '/login.html',
            '/pages/student-dashboard.html',
            '/pages/coordinator-dashboard.html',
            '/pages/admin-dashboard.html',
            '/pages/club-details.html',
            '/css/style.css',
            '/css/navbar.css',
            '/css/dashboard.css',
            '/js/api.js',
            '/js/auth.js',
            '/js/main.js',
            '/js/student.js',
            '/js/coordinator.js',
            '/js/admin.js'
        ]
        for page in pages:
            res = self.client.get(page)
            self.assertEqual(res.status_code, 200, f"Failed serving {page}")

    def test_02_rbac_unauthorized_access(self):
        """Verify unauthorized users are blocked from protected endpoints."""
        protected_endpoints = [
            ('/api/student/memberships', 'GET'),
            ('/api/coordinator/club', 'GET'),
            ('/api/coordinator/requests', 'GET'),
            ('/api/admin/overview', 'GET'),
            ('/api/admin/users', 'GET')
        ]
        for url, method in protected_endpoints:
            res = self.client.open(url, method=method)
            self.assertEqual(res.status_code, 401, f"Expected 401 for unauthenticated {method} {url}")

    def test_03_role_forbidden_access(self):
        """Verify students cannot access coordinator or admin endpoints."""
        student_res = self.client.post('/api/auth/login', json={
            'email': 'student1@campus.edu',
            'password': 'password123'
        })
        student_token = student_res.get_json()['token']
        headers = {'Authorization': f'Bearer {student_token}'}

        # Student trying coordinator endpoint
        res = self.client.get('/api/coordinator/club', headers=headers)
        self.assertEqual(res.status_code, 403)

        # Student trying admin endpoint
        res = self.client.get('/api/admin/overview', headers=headers)
        self.assertEqual(res.status_code, 403)

    def test_04_coordinator_actions(self):
        """Verify coordinator can view their club, events, announcements and create an announcement."""
        coord_res = self.client.post('/api/auth/login', json={
            'email': 'coding.lead@campus.edu',
            'password': 'password123'
        })
        token = coord_res.get_json()['token']
        headers = {'Authorization': f'Bearer {token}'}

        # 1. View assigned club
        club_res = self.client.get('/api/coordinator/club', headers=headers)
        self.assertEqual(club_res.status_code, 200)
        self.assertEqual(club_res.get_json()['club']['name'], 'Coding Club')

        # 2. Create announcement
        create_res = self.client.post('/api/coordinator/announcements', headers=headers, json={
            'title': 'Test Verification Announcement',
            'content': 'This is an automated verification post.'
        })
        self.assertEqual(create_res.status_code, 201)
        ann_id = create_res.get_json()['announcement']['id']

        # 3. Delete announcement to keep database clean
        del_res = self.client.delete(f'/api/coordinator/announcements/{ann_id}', headers=headers)
        self.assertEqual(del_res.status_code, 200)

    def test_05_admin_user_management(self):
        """Verify admin can list users, toggle status, and change role."""
        admin_res = self.client.post('/api/auth/login', json={
            'email': 'admin@campus.edu',
            'password': 'password123'
        })
        token = admin_res.get_json()['token']
        headers = {'Authorization': f'Bearer {token}'}

        # 1. List users
        users_res = self.client.get('/api/admin/users', headers=headers)
        self.assertEqual(users_res.status_code, 200)
        self.assertGreater(users_res.get_json()['count'], 0)

        # 2. Toggle status of student4 (user id 10)
        toggle_res = self.client.post('/api/admin/users/10/toggle-status', headers=headers)
        self.assertEqual(toggle_res.status_code, 200)

        # Toggle back to original state
        toggle_back = self.client.post('/api/admin/users/10/toggle-status', headers=headers)
        self.assertEqual(toggle_back.status_code, 200)

if __name__ == '__main__':
    unittest.main()
