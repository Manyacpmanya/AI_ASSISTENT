CREATE DATABASE ai_sql_db;
USE ai_sql_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    usn VARCHAR(20),
    branch VARCHAR(50)
);

CREATE TABLE student_academics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    cgpa FLOAT,
    FOREIGN KEY (student_id) REFERENCES users(id)
);

INSERT INTO users (name, usn, branch) VALUES
('Ramesh', '4GW22CS001', 'CSE'),
('Suresh', '4GW22CS002', 'CSE');

INSERT INTO student_academics (student_id, cgpa) VALUES
(1, 9.1),
(2, 8.5);
