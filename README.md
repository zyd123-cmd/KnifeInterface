FastAPI 多角色接口二次封装项目

项目简介

这是一个基于 FastAPI 的接口二次封装项目，针对三种不同角色（管理员、审计员、操作员）提供了独立的接口封装服务。项目采用模块化设计，每个角色拥有独立的数据模型、服务逻辑和路由处理。

项目特性

• 🏗️ 多角色架构：支持 administrator、auditor、operator 三种角色

• 📦 模块化设计：各角色功能独立，便于维护和扩展

• 🔒 类型安全：使用 Pydantic 模型进行数据验证

• 📚 自动文档：FastAPI 自动生成交互式 API 文档

• ⚡ 高性能：支持异步请求处理

• 🔧 配置灵活：通过环境变量管理配置

项目结构


project/
├── administrator/          # 管理员角色模块
│   ├── schemas/           # 数据模型定义
│   │   └── data_schemas.py
│   └── services/          # 服务逻辑
│       ├── api_client.py  # API客户端封装
│       └── main.py        # 管理员服务入口
├── auditor/               # 审计员角色模块
│   ├── schemas/
│   │   └── data_schemas.py
│   └── services/
│       └── api_client.py
├── operator/              # 操作员角色模块
│   ├── schemas/
│   │   └── data_schemas.py
│   ├── services/
│   │   └── api_client.py
│   └── routers/           # 路由定义
│       └── data_router.py
└── config/               # 配置文件
    ├── .env              # 环境变量
    └── config.py         # 配置加载


环境要求

• Python 3.8+

• FastAPI

• Uvicorn

• Requests

• Python-dotenv

安装依赖

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/MacOS
source venv/bin/activate
# Windows
venv\Scripts\activate

# 安装依赖
pip install fastapi uvicorn requests python-dotenv


配置说明

1. 复制 config/.env.example 为 config/.env
2. 根据实际环境配置以下变量：
# API 配置
API_TITLE=多角色接口服务
API_DESCRIPTION=基于FastAPI的多角色接口二次封装服务
API_VERSION=1.0.0

# 原始API配置
ORIGINAL_API_BASE_URL=https://api.example.com
ORIGINAL_API_KEY=your_api_key_here

# 服务器配置
HOST=0.0.0.0
PORT=8000
DEBUG=False


运行项目

启动管理员服务

cd administrator/services
uvicorn main:app --reload --host 0.0.0.0 --port 8000


启动操作员服务

cd operator/services
uvicorn api_client:app --reload --host 0.0.0.0 --port 8001


访问API文档

• 管理员接口文档: http://localhost:8000/docs

• 操作员接口文档: http://localhost:8001/docs

角色功能说明

Administrator (管理员)

• 最高权限角色

• 完整的系统管理功能

• 用户和权限管理

• 系统配置管理

Auditor (审计员)

• 数据查看和审计功能

• 操作日志查询

• 系统状态监控

• 只读权限，无修改功能

Operator (操作员)

• 日常操作功能

• 业务数据处理

• 有限的系统操作权限

• 通过路由暴露业务接口

开发指南

添加新模型

1. 在对应角色的 schemas/data_schemas.py 中添加 Pydantic 模型
2. 在服务层实现相关业务逻辑
3. 在路由层暴露接口（如为 operator 角色）

调用原始API

使用各角色 services 目录下的 api_client.py 中封装的客户端方法：
from operator.services.api_client import original_api_client

# 调用原始API
data = original_api_client.get_data(endpoint="users/123")


添加新接口

对于 operator 角色，在 routers/data_router.py 中添加新路由：
@router.get("/new-endpoint")
async def new_endpoint():
    # 业务逻辑
    return {"message": "New endpoint"}


部署建议

生产环境部署

# 使用Gunicorn运行（生产环境）
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000


Docker 部署

FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "administrator.services.main:app", "--host", "0.0.0.0", "--port", "8000"]


注意事项

1. 各角色的 .env 配置需要根据实际部署环境进行调整
2. 生产环境请设置 DEBUG=False
3. 建议为每个角色使用不同的端口号
4. 原始API的认证信息需要妥善保管

故障排除

1. 端口冲突：修改配置中的端口号
2. 依赖问题：确保所有依赖包已正确安装
3. API连接失败：检查原始API的基地址和认证信息
4. 模块导入错误：确保正确设置Python路径
