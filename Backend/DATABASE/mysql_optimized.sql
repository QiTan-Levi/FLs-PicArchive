-- 用户表
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    avatar_id VARCHAR(24) COMMENT 'MongoDB中存储的头像文件ID',
    RegisTime DATETIME NOT NULL,
    last_login DATETIME,
    status TINYINT DEFAULT 1 COMMENT '1-正常 0-禁用'
);

-- 图片表
CREATE TABLE images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    file_id VARCHAR(24) NOT NULL COMMENT 'MongoDB中存储的图片文件ID',
    aircraft_model VARCHAR(100),
    location VARCHAR(255),
    shooting_time DATETIME,
    description TEXT,
    upload_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status TINYINT DEFAULT 0 COMMENT '0-待审核 1-已通过 2-已拒绝',
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 评论表
CREATE TABLE comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    image_id INT NOT NULL,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    comment_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (image_id) REFERENCES images(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 审图任务表
CREATE TABLE review_tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    image_id INT NOT NULL,
    reviewer_id INT NOT NULL,
    result TINYINT COMMENT '1-通过 0-拒绝',
    score TINYINT COMMENT '1-5分',
    review_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    remarks TEXT,
    FOREIGN KEY (image_id) REFERENCES images(id),
    FOREIGN KEY (reviewer_id) REFERENCES users(id)
);

-- 审图方案表
CREATE TABLE review_schemes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    rules JSON COMMENT '存储JSON格式的审核规则',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME ON UPDATE CURRENT_TIMESTAMP
);

-- 系统日志表
CREATE TABLE system_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operator_id INT,
    operation VARCHAR(50) NOT NULL,
    content TEXT,
    result TINYINT COMMENT '1-成功 0-失败',
    ip_address VARCHAR(50),
    operation_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (operator_id) REFERENCES users(id)
);