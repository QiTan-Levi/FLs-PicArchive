-- 检查 users 表是否存在，如果不存在则创建
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY, -- 用户ID
    username VARCHAR(50) NOT NULL UNIQUE, -- 用户名
    password VARCHAR(255) NOT NULL, -- 密码
    email VARCHAR(100) NOT NULL UNIQUE, -- 邮箱
    avatar VARCHAR(255) COMMENT "用户头像", -- 用户头像
    regis_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 注册时间
    last_login DATETIME, -- 上次登录时间
    status TINYINT DEFAULT 1 COMMENT '0-禁用 1-正常 2-审图员 3-管理员' -- 用户状态
);

-- 检查 images 表是否存在，如果不存在则创建
CREATE TABLE IF NOT EXISTS images (
    -- 图片的唯一标识
    id INT AUTO_INCREMENT PRIMARY KEY,
    -- 用户的唯一标识
    user_id INT NOT NULL,
    -- 拍摄的具体时间
    shooting_time DATETIME,
    -- 拍摄时间所对应的时区
    timezone VARCHAR(50),
    -- 飞机的注册号
    registration_number VARCHAR(50),
    -- 当时执行航班号
    flight_number VARCHAR(50),
    -- 航司或运营人名称
    airline_operator VARCHAR(255),
    -- 飞机的机型
    aircraft_model VARCHAR(255),
    -- 图片类型
    image_type SET('Airport', 'Cockpit', 'Artistic', 'Ground', 'Cargo', 'Special_Livery', 'Night','Nospecial') NOT NULL DEFAULT 'Nospecial',
    -- 天气状况（建议以当时ATIS为准，若未知则以图片为准）
    weather SET('Sunny', 'Cloudy', 'Overcast', 'Rain', 'Snow', 'Fog', 'Haze', 'Freezing', 'Hail') NOT NULL,
    -- 图片的描述
    image_description TEXT,
    -- 图片的位置信息
    location VARCHAR(255),
    -- 图片的上传时间
    upload_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- 是否为精选图片
    is_featured TINYINT DEFAULT 0 COMMENT '0-普通 1-精选',
    -- 审核评星
    rating TINYINT DEFAULT 0 COMMENT '0-未评 1-一星 2-两星 3-三星',
    -- 图片的文件类型，限定为 jpg/jpeg
    file_type ENUM('jpg', 'jpeg') NOT NULL,
    -- 审核人/待审核人
    reviewer_id INT,
    -- 审核时间
    review_time DATETIME,
    -- 图片数据，以 BLOB 类型存储，最大可存储 30MB
    image_data LONGBLOB NOT NULL,
    -- 用于区分图片是待审核还是已审核
    is_pending TINYINT DEFAULT 1 COMMENT '1-待审核 0-已审核',
    -- 外键约束，关联 users 表的 id 字段
    FOREIGN KEY (user_id) REFERENCES users(id),
    -- 为 registration_number 字段创建索引，提高查询效率
    INDEX idx_registration_number (registration_number),
    -- 为 aircraft_model 字段创建索引，提高查询效率
    INDEX idx_aircraft_model (aircraft_model),
    -- 为 airline_operator 字段创建索引，提高查询效率
    INDEX idx_airline_operator (airline_operator),
    -- 为 location 字段创建索引，提高查询效率
    INDEX idx_location (location)
);

-- 检查 comments 表是否存在，如果不存在则创建
CREATE TABLE IF NOT EXISTS comments (
    -- 评论、点赞ID
    id INT AUTO_INCREMENT PRIMARY KEY,
    -- 类型
    type TINYINT DEFAULT 0 COMMENT '0-评论 1-点赞',
    -- 图片ID
    image_id INT NOT NULL,
    -- 用户ID
    user_id INT NOT NULL,
    -- 评论内容
    content TEXT,
    -- 评论时间
    comment_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- 外键关联图片表
    FOREIGN KEY (image_id) REFERENCES images(id),
    -- 外键关联用户表
    FOREIGN KEY (user_id) REFERENCES users(id),
    -- 评论内容不能为空，点赞内容可以为空
    CHECK ((type = 0 AND content IS NOT NULL) OR (type = 1))
);

-- 检查 system_logs 表是否存在，如果不存在则创建
CREATE TABLE IF NOT EXISTS system_logs (
    -- 操作ID
    id INT AUTO_INCREMENT PRIMARY KEY,
    -- 操作人ID
    operator_id INT,
    -- 图片ID
    image_id INT,
    -- 操作内容
    operation VARCHAR(50) NOT NULL,
    -- 操作详情
    content TEXT,
    -- 操作结果
    result TINYINT COMMENT '1-成功 0-失败',
    -- 操作IP地址
    ip_address VARCHAR(50),
    -- 操作时间
    operation_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- 外键关联用户表
    FOREIGN KEY (operator_id) REFERENCES users(id),
    -- 外键关联图片表
    FOREIGN KEY (image_id) REFERENCES images(id)
);