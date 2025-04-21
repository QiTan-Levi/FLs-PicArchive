# FocusLevi's Picture Archive System

## 项目简介
FocusLevi's Picture Archive System 是一个专注于航空图片管理的综合性系统，旨在为航空爱好者、摄影师及相关专业人士提供高效、便捷的图片管理与交流平台。系统采用前沿的前端和后端技术，结合精心设计的数据库架构，实现图片的高效管理、用户交互以及专业的审图流程，满足不同用户群体的多样化需求。

## 技术选型
### 前端技术
- **框架**：Vue.js
- **路由管理**：Vue Router
- **状态管理**：Vuex

### 后端技术
- **框架**：Flask
- **数据库交互**：PyMySQL（MySQL）
- 【暂未使用】**身份验证**：JWT
- 【暂未使用】**异步处理**：Celery

## 数据库设计
### MySQL 数据库
- **用户表（users）**：存储用户基本信息，包括用户名、密码、邮箱、头像、注册时间、上次登录时间和用户状态。
- **图片表（images）**：记录图片详细信息，包括用户ID、拍摄时间、时区、飞机注册号、航班号、航司名称、飞机机型、图片类型、天气状况、图片描述、位置信息、上传时间、是否精选、文件类型、审核人、审核时间、图片数据和审核状态。
- **评论表（comments）**：保存图片评论数据，包括评论或点赞ID、类型、图片ID、用户ID、评论内容和评论时间。
- **系统日志表（system_logs）**：记录系统操作日志，包括操作ID、操作人ID、图片ID、操作内容、操作详情、操作结果、操作IP地址和操作时间。


## 安装与运行
### 前置条件
- Python 3.8+
- Node.js 14+
- MySQL 8+

### 安装步骤
1. **克隆项目**：
   ```bash
   git clone https://github.com/QiTan-Levi/FLs-PicArchive/.git
   cd FocusLevi's-Picture-Archive-System
   ```
2. **安装依赖**：
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
   ```bash
   cd frontend
   npm install
   ```
3. **配置数据库连接信息**：
   - 后端：修改 `backend/config.py` 中的数据库连接信息。

4. **启动服务**：
   ```bash
   # 后端
   cd backend
   python app.py
   #前端
   cd frontend
   npm run serve
   ```
## 使用说明
### 用户注册与登录
- 访问 /account/register 页面进行注册。
- 访问 /account/login 页面进行登录。
### 系统管理
- 管理员登录后，访问 /admin 页面进行系统管理。
- 功能待定。
## 未来计划
- **优化**：加载速度
- **优化**：性能负荷
- **优化**：界面设计，增加动画
- **优化**：交互设计 
- **增加**：头像功能
- **增加**：图片上传后自动增加水印功能
  - **扩展**：自己设计水印放哪，大小，透明度
  - **扩展**：同时使用上传者和平台水印并存
- **增加**：语言本地化
- **复用**：铁路图库
- **扩展**：复用：通用化，图床

## 联系方式
- 项目主页 ： https://github.com/QiTan-Levi/FLs-PicArchive/
- 邮箱 ： FocusLevi@163.com
- 作者 ： FocusLevi
---
任何疑问请提issue，项目出错请发邮件。谢谢支持。