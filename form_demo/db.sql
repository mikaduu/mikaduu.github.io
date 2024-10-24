-- 创建 users 数据库
CREATE DATABASE IF NOT EXISTS users;

USE users;

-- 创建 users 表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tips TEXT
);

-- 创建 posts 数据库
CREATE DATABASE IF NOT EXISTS posts;

USE posts;

-- 创建 posts 表
CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    visit INT DEFAULT 0,
    likes INT DEFAULT 0,
    writer VARCHAR(50) NOT NULL,
    FOREIGN KEY (writer) REFERENCES users.users(username) ON DELETE CASCADE ON UPDATE CASCADE
);