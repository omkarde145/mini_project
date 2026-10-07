-- =============================================================================
-- Club Management System - Seed Data (DML)
-- All seed accounts use password: password123
-- =============================================================================

USE `club_management_db`;

-- -----------------------------------------------------------------------------
-- Seed: users
-- Passwords: password123
-- Hash: scrypt:32768:8:1$oQw9gBBVE45TXgXZ$4a56daedebcb10927420973fada63ee6793ceaa1002463446c2a5e137ccc1e598661fa372158f0916b47271f21203870cc65b0ca5a83556f5a4a9591b492dcab
-- -----------------------------------------------------------------------------
INSERT INTO `users` (`id`, `full_name`, `email`, `password_hash`, `role`, `is_active`, `department`, `student_id`, `phone`) VALUES
-- Admin
(1, 'System Administrator', 'admin@campus.edu', 'scrypt:32768:8:1$oQw9gBBVE45TXgXZ$4a56daedebcb10927420973fada63ee6793ceaa1002463446c2a5e137ccc1e598661fa372158f0916b47271f21203870cc65b0ca5a83556f5a4a9591b492dcab', 'admin', TRUE, 'Administration', 'ADM-001', '+1-555-0100'),

-- Coordinators
(2, 'Alex Rivera', 'coding.lead@campus.edu', 'scrypt:32768:8:1$oQw9gBBVE45TXgXZ$4a56daedebcb10927420973fada63ee6793ceaa1002463446c2a5e137ccc1e598661fa372158f0916b47271f21203870cc65b0ca5a83556f5a4a9591b492dcab', 'coordinator', TRUE, 'Computer Science', 'CS-2022-041', '+1-555-0101'),
(3, 'Elena Rostova', 'robotics.lead@campus.edu', 'scrypt:32768:8:1$oQw9gBBVE45TXgXZ$4a56daedebcb10927420973fada63ee6793ceaa1002463446c2a5e137ccc1e598661fa372158f0916b47271f21203870cc65b0ca5a83556f5a4a9591b492dcab', 'coordinator', TRUE, 'Mechanical & Electrical Eng', 'ENG-2021-089', '+1-555-0102'),
(4, 'Marcus Chen', 'arts.lead@campus.edu', 'scrypt:32768:8:1$oQw9gBBVE45TXgXZ$4a56daedebcb10927420973fada63ee6793ceaa1002463446c2a5e137ccc1e598661fa372158f0916b47271f21203870cc65b0ca5a83556f5a4a9591b492dcab', 'coordinator', TRUE, 'Visual & Performing Arts', 'ART-2023-014', '+1-555-0103'),
(5, 'Sophia Patel', 'music.lead@campus.edu', 'scrypt:32768:8:1$oQw9gBBVE45TXgXZ$4a56daedebcb10927420973fada63ee6793ceaa1002463446c2a5e137ccc1e598661fa372158f0916b47271f21203870cc65b0ca5a83556f5a4a9591b492dcab', 'coordinator', TRUE, 'Humanities & Music', 'MUS-2022-055', '+1-555-0104'),
(6, 'David Kim', 'eco.lead@campus.edu', 'scrypt:32768:8:1$oQw9gBBVE45TXgXZ$4a56daedebcb10927420973fada63ee6793ceaa1002463446c2a5e137ccc1e598661fa372158f0916b47271f21203870cc65b0ca5a83556f5a4a9591b492dcab', 'coordinator', TRUE, 'Environmental Sciences', 'ENV-2023-072', '+1-555-0105'),

-- Students
(7, 'Sarah Jenkins', 'student1@campus.edu', 'scrypt:32768:8:1$oQw9gBBVE45TXgXZ$4a56daedebcb10927420973fada63ee6793ceaa1002463446c2a5e137ccc1e598661fa372158f0916b47271f21203870cc65b0ca5a83556f5a4a9591b492dcab', 'student', TRUE, 'Computer Science', 'STU-2024-101', '+1-555-0201'),
(8, 'Liam O''Connor', 'student2@campus.edu', 'scrypt:32768:8:1$oQw9gBBVE45TXgXZ$4a56daedebcb10927420973fada63ee6793ceaa1002463446c2a5e137ccc1e598661fa372158f0916b47271f21203870cc65b0ca5a83556f5a4a9591b492dcab', 'student', TRUE, 'Business Administration', 'STU-2024-102', '+1-555-0202'),
(9, 'Aaliyah Khan', 'student3@campus.edu', 'scrypt:32768:8:1$oQw9gBBVE45TXgXZ$4a56daedebcb10927420973fada63ee6793ceaa1002463446c2a5e137ccc1e598661fa372158f0916b47271f21203870cc65b0ca5a83556f5a4a9591b492dcab', 'student', TRUE, 'Data Science', 'STU-2024-103', '+1-555-0203'),
(10, 'Noah Williams', 'student4@campus.edu', 'scrypt:32768:8:1$oQw9gBBVE45TXgXZ$4a56daedebcb10927420973fada63ee6793ceaa1002463446c2a5e137ccc1e598661fa372158f0916b47271f21203870cc65b0ca5a83556f5a4a9591b492dcab', 'student', FALSE, 'Physics', 'STU-2024-104', '+1-555-0204');

-- -----------------------------------------------------------------------------
-- Seed: clubs
-- -----------------------------------------------------------------------------
INSERT INTO `clubs` (`id`, `name`, `description`, `category`, `banner_url`, `coordinator_id`, `status`) VALUES
(1, 'Coding Club', 'Campus premier hub for software engineering, competitive programming, open source projects, and tech interview prep.', 'Technology', 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=1200&auto=format&fit=crop&q=80', 2, 'approved'),
(2, 'Robotics Society', 'Dedicated to autonomous robotics, aerial drones, IoT systems, and competing in collegiate robotics championships.', 'Technology', 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=1200&auto=format&fit=crop&q=80', 3, 'approved'),
(3, 'Fine Arts Guild', 'A creative sanctuary for sketch artists, digital illustrators, sculptors, and multimedia painters across campus.', 'Arts & Culture', 'https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?w=1200&auto=format&fit=crop&q=80', 4, 'approved'),
(4, 'Echo Music Collective', 'Uniting instrumentalists, vocalists, audio engineers, and indie bands for live concerts and collaborative jam sessions.', 'Music', 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=1200&auto=format&fit=crop&q=80', 5, 'approved'),
(5, 'Eco Action League', 'Promoting campus sustainability, tree plantation drives, waste reduction initiatives, and climate awareness.', 'Environment', 'https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=1200&auto=format&fit=crop&q=80', 6, 'pending'),
(6, 'Debate & Oratory Union', 'Sharpening critical thought, policy analysis, and competitive forensics through intercollegiate parliamentary debate.', 'Academic', 'https://images.unsplash.com/photo-1475721027785-f74eccf877e2?w=1200&auto=format&fit=crop&q=80', NULL, 'pending');

-- -----------------------------------------------------------------------------
-- Seed: memberships
-- -----------------------------------------------------------------------------
INSERT INTO `memberships` (`id`, `user_id`, `club_id`, `status`, `applied_at`, `reviewed_at`) VALUES
-- Sarah Jenkins memberships
(1, 7, 1, 'approved', '2026-09-10 10:00:00', '2026-09-11 14:00:00'),
(2, 7, 2, 'pending', '2026-10-01 11:30:00', NULL),

-- Liam O'Connor memberships
(3, 8, 1, 'approved', '2026-09-12 09:15:00', '2026-09-13 16:20:00'),
(4, 8, 3, 'pending', '2026-10-02 14:45:00', NULL),
(5, 8, 4, 'rejected', '2026-09-15 12:00:00', '2026-09-16 10:30:00'),

-- Aaliyah Khan memberships
(6, 9, 2, 'approved', '2026-09-14 15:20:00', '2026-09-15 11:00:00'),
(7, 9, 1, 'pending', '2026-10-04 16:10:00', NULL);

-- -----------------------------------------------------------------------------
-- Seed: events
-- -----------------------------------------------------------------------------
INSERT INTO `events` (`id`, `club_id`, `title`, `description`, `event_date`, `location`) VALUES
(1, 1, 'Annual Hackathon 2026: CodeWave', '36-hour sprint creating AI-driven campus utilities and social impact software. Mentors and prizes provided.', '2026-10-25 09:00:00', 'Science & Technology Hall, Room 301'),
(2, 1, 'Git & GitHub Fundamentals Workshop', 'Hands-on crash course on version control, pull requests, merge conflict resolution, and open source hygiene.', '2026-10-14 17:00:00', 'Computer Lab 4B'),
(3, 1, 'Python Web Dev with Flask & FastAPI', 'Past seminar covering modern microservices, database transactions, and scalable web architectures.', '2026-09-20 18:00:00', 'Online via Zoom'),

(4, 2, 'Autonomous Drone Navigation Demo', 'Live flight obstacle course exhibition using computer vision and LiDAR telemetry on custom quadcopters.', '2026-10-28 15:30:00', 'Campus Quadrangle West'),
(5, 2, 'Arduino & ESP32 Embedded Systems Bootcamp', 'Introductory hardware wiring, sensor calibration, and Wi-Fi IoT telemetry workshop.', '2026-11-05 14:00:00', 'Robotics Makerspace B12'),

(6, 3, 'Autumn Plein Air Canvas Exhibition', 'Outdoor painting gallery showcasing student watercolor and acrylic works inspired by campus flora.', '2026-10-30 11:00:00', 'Fine Arts Courtyard'),

(7, 4, 'Acoustic Jam Night & Open Mic', 'Relaxed acoustic evening welcoming singers, songwriters, and multi-instrumentalists.', '2026-10-22 19:30:00', 'Student Union Amphitheater');

-- -----------------------------------------------------------------------------
-- Seed: announcements
-- -----------------------------------------------------------------------------
INSERT INTO `announcements` (`id`, `club_id`, `title`, `content`, `posted_at`) VALUES
(1, 1, 'CodeWave 2026 Registration is Now Open!', 'Team registrations are now officially live. Teams of up to 4 can apply on the portal. Bring your laptops, chargers, and creative ideas!', '2026-10-05 08:30:00'),
(2, 1, 'Weekly LeetCode & DSA Meetup', 'Join us every Wednesday at 6 PM in Lab 4B for weekly problem-solving and whiteboarding sessions.', '2026-10-02 12:00:00'),

(3, 2, 'Robotics Lab Equipment Update', 'New 3D printers and soldering stations have been installed in Makerspace B12. Please complete safety training before operating.', '2026-10-04 10:15:00'),

(4, 3, 'Call for Artworks: Campus Magazine Cover', 'Submit your digital or traditional illustrations for the upcoming winter edition of the Campus Quarterly Magazine.', '2026-10-03 14:00:00'),

(5, 4, 'Auditions for Spring Campus Band Roster', 'Vocalists, bassists, and drum kit players: book an audition slot for upcoming inter-collegiate festival tours.', '2026-10-06 17:00:00');
