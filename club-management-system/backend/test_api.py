import unittest
import json
from app import create_app

class ClubSystemApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_health_check(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')

    def test_browse_clubs(self):
        response = self.client.get('/api/student/clubs')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertGreater(data['count'], 0)

    def test_login_student(self):
        response = self.client.post('/api/auth/login', json={
            'email': 'student1@campus.edu',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['user']['role'], 'student')
        self.assertIn('token', data)

    def test_login_coordinator(self):
        response = self.client.post('/api/auth/login', json={
            'email': 'coding.lead@campus.edu',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['user']['role'], 'coordinator')
        self.assertIsNotNone(data['club'])
        self.assertEqual(data['club']['name'], 'Coding Club')

    def test_login_admin(self):
        response = self.client.post('/api/auth/login', json={
            'email': 'admin@campus.edu',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['user']['role'], 'admin')

    def test_student_join_request_flow(self):
        # 1. Login as student3
        login_res = self.client.post('/api/auth/login', json={
            'email': 'student3@campus.edu',
            'password': 'password123'
        })
        token = login_res.get_json()['token']
        headers = {'Authorization': f'Bearer {token}'}

        # 2. Ensure test state is clean before joining club 3 (Fine Arts Guild)
        from models.membership import Membership
        Membership.remove_member(3, 9)

        join_res = self.client.post('/api/student/clubs/3/join', headers=headers)
        self.assertIn(join_res.status_code, [200, 201])

        # 3. Check my memberships
        mem_res = self.client.get('/api/student/memberships', headers=headers)
        self.assertEqual(mem_res.status_code, 200)
        mems = mem_res.get_json()['memberships']
        fine_arts = [m for m in mems if m['club_id'] == 3]
        self.assertEqual(len(fine_arts), 1)
        self.assertEqual(fine_arts[0]['status'], 'pending')

    def test_admin_overview_metrics(self):
        login_res = self.client.post('/api/auth/login', json={
            'email': 'admin@campus.edu',
            'password': 'password123'
        })
        token = login_res.get_json()['token']
        headers = {'Authorization': f'Bearer {token}'}

        overview_res = self.client.get('/api/admin/overview', headers=headers)
        self.assertEqual(overview_res.status_code, 200)
        metrics = overview_res.get_json()['metrics']
        self.assertGreater(metrics['total_clubs'], 0)
        self.assertGreater(metrics['total_students'], 0)

if __name__ == '__main__':
    unittest.main()
