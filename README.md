# FocusLevi's Picture Archive System

## 项目简介
FocusLevi's Picture Archive System 是一个专注于航空图片管理的综合性系统，旨在为航空爱好者、摄影师及相关专业人士提供高效、便捷的图片管理与交流平台。系统采用前沿的前端和后端技术，结合精心设计的数据库架构，实现图片的高效管理、用户交互以及专业的审图流程，满足不同用户群体的多样化需求。

## 功能模块
### 前端功能模块
- **主页**：支持图片搜索、筛选、点赞、收藏、推荐等功能，展示热门和最新图片。
- **上传页**：提供图片上传、格式和大小验证、预览、信息填写与验证、分类建议等功能。
- **文档页**：实现文档分类展示、搜索、收藏、分享等功能。
- **账号页**：支持个人信息修改、密码修改、查看上传历史和收藏图片、账号安全提醒等功能。
- **图片详情页**：提供图片放大缩小、分享、评论、点赞、图片对比等功能。
- **审图员页面**：包括已审图片筛选、详情查看、审核结果统计分析、图片标注、打分、批注、选择审核结果、提交审核、审图模板选择等功能。
- **管理员页面**：实现审图任务分配、查看与修改、任务数量和完成情况统计、任务优先级设置、审图方案管理、系统管理等功能。

### 后端功能模块
- **用户管理**：支持用户注册、登录、信息更新等功能。
- **图片管理**：提供图片上传、获取、删除等功能。
- **审图管理**：实现审图任务分配、结果收集、方案管理等功能。
- **数据库管理**：支持数据库连接、数据迁移等功能。
- **系统监控与日志管理**：提供系统性能监控、预警、日志记录与管理等功能。

## 技术选型
### 前端技术
- **框架**：Vue.js
- **路由管理**：Vue Router
- **状态管理**：Vuex
- **UI 框架**：Tailwind CSS
- **图标库**：Font Awesome

### 后端技术
- **框架**：Flask
- **数据库交互**：SQLAlchemy（MySQL）、PyMongo（MongoDB）
- **身份验证**：JWT
- **异步处理**：Celery

## 数据库设计
### MySQL 数据库
- **用户表（users）**：存储用户基本信息。
- **图片表（images）**：记录图片详细信息。
- **评论表（comments）**：保存图片评论数据。
- **审图任务表（review_tasks）**：跟踪审图任务分配和完成情况。
- **审图方案表（review_schemes）**：管理审图方案。
- **系统日志表（system_logs）**：记录系统操作日志。

### MongoDB 数据库
- **用户集合（users）**：以 JSON 格式存储用户信息。
- **图片集合（images）**：存储图片元数据。
- **评论集合（comments）**：保存图片评论信息。
- **审图任务集合（review_tasks）**：记录审图任务数据。
- **审图方案集合（review_schemes）**：存储审图方案。
- **系统监控集合（system_monitoring）**：存储系统监控数据。

## 项目结构
```
FocusLevi's Picture Archive System/
│
├── frontend/                  # 前端代码目录
│   ├── src/                   # Vue.js 源代码
│   │   ├── components/        # Vue 组件
│   │   ├── views/             # 页面视图
│   │   ├── store/             # Vuex 状态管理
│   │   ├── router/            # Vue Router 路由配置
│   │   └── main.js            # 入口文件
│   ├── public/                # 静态资源
│   └── package.json           # 依赖管理
│
├── backend/                   # 后端代码目录
│   ├── app.py                 # Flask 应用入口
│   ├── utils/                 # 工具函数和数据库连接
│   ├── uploads/               # 上传文件存储路径
│   └── requirements.txt       # Python 依赖管理
│
├── README.md                  # 项目说明文档
├── .env                       # 环境变量配置
└── docker-compose.yml         # Docker 容器配置
```

## 安装与运行
### 前置条件
- Python 3.8+
- Node.js 14+
- MySQL 8+
- MongoDB 4+
- Docker（可选）

### 安装步骤
1. **克隆项目**：
   ```bash
   git clone https://github.com/QiTan-Levi/FLs-PicArchive/.git
   cd FocusLevi's-Picture-Archive-System
   ```

2. **安装前端依赖**：
   ```bash
   cd frontend
   npm install
   ```

3. **安装后端依赖**：
   ```bash
   cd ../backend
   pip install -r requirements.txt
   ```

4. **配置数据库**：
   - 创建 MySQL 数据库和用户。
   - 创建 MongoDB 数据库和用户。
   - 修改 `.env` 文件，配置数据库连接信息。

5. **运行项目**：
   - **前端**：
     ```bash
     cd frontend
     npm run serve
     ```
   - **后端**：
     ```bash
     cd backend
     python app.py
     ```

6. **使用 Docker 运行**（可选）：
   ```bash
   docker-compose up --build
   ```

## 使用说明
### 用户注册与登录
- 访问 `/account/register` 页面进行注册。
- 访问 `/account/login` 页面进行登录。

### 图片上传
- 登录后，访问 `/upload` 页面上传图片。
- 填写图片相关信息并提交。

### 图片搜索与筛选
- 在主页搜索框输入关键词进行搜索。
- 使用筛选条件进一步筛选图片。

### 图片审图
- 审图员登录后，访问 `/review` 页面进行图片审核。
- 对图片进行标注、打分、批注并提交审核结果。

### 系统管理
- 管理员登录后，访问 `/admin` 页面进行系统管理。
- 包括审图任务分配、审图方案管理、数据库配置等功能。

## 技术难点与解决方案
### 图片处理和存储
- **难点**：处理不同格式和大小的图片，保证图片质量和存储效率。
- **解决方案**：使用 Pillow 库对图片进行压缩和裁剪，存储到本地或云存储（如 Amazon S3）。

### 并发处理
- **难点**：大量用户同时上传图片或进行搜索时，系统响应延迟。
- **解决方案**：采用 Celery 进行异步任务处理，使用 Redis 缓存常用数据。

### 数据一致性
- **难点**：MySQL 和 MongoDB 数据同步时可能出现数据不一致。
- **解决方案**：使用数据同步工具（如 Canal），采用分布式事务管理框架（如 Seata）。

## 未来展望
- **功能扩展**：增加更多图片处理功能，如图片编辑、特效添加等。
- **性能优化**：进一步优化图片加载速度和系统并发处理能力。
- **用户体验提升**：优化界面设计，增加更多交互效果。
- **国际化支持**：支持多语言界面，满足全球用户需求。

## 贡献指南
欢迎贡献代码或提出改进建议！请遵循以下步骤：
1. Fork 本项目。
2. 创建新分支：`git checkout -b feature/your-feature-name`。
3. 提交更改：`git commit -m "Add some feature"`。
4. 推送分支：`git push origin feature/your-feature-name`。
5. 提交 Pull Request。

## 联系方式
- **项目主页**：[https://github.com/QiTan-Levi/FLs-PicArchive/](https://github.com/QiTan-Levi/FLs-PicArchive/)
- **邮箱**：[FocusLevi@163.com](mailto:FocusLevi@163.com)
- **作者**：[FocusLevi](https://github.com/QiTan-Levi/)

---

感谢您的支持！