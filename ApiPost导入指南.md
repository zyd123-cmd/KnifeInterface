# ApiPost 导入 FastAPI 接口文档指南

## 📋 目录

1. [方法一：通过 OpenAPI JSON 导入（推荐）](#方法一通过-openapi-json-导入推荐)
2. [方法二：使用 FastAPI 内置文档](#方法二使用-fastapi-内置文档)
3. [优化后的功能](#优化后的功能)
4. [常见问题](#常见问题)

---

## 方法一：通过 OpenAPI JSON 导入（推荐）

### ✅ 步骤 1：启动 FastAPI 服务

打开终端，执行以下命令：

```bash
cd /Users/linhe/PycharmProjects/KnifeInterface
python knife_operator/main.py
```

**预期输出**：
```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
```

### ✅ 步骤 2：获取 OpenAPI JSON 文档

服务启动后，FastAPI 自动生成了 OpenAPI 规范的 JSON 文档。

**方式 A：浏览器查看**
1. 打开浏览器
2. 访问：`http://localhost:8001/openapi.json`
3. 您会看到完整的 JSON 格式 API 文档

**方式 B：保存到文件（推荐）**
```bash
# 在新的终端窗口执行
curl http://localhost:8001/openapi.json > knife_operator_api.json
```

### ✅ 步骤 3：在 ApiPost 中导入

#### 选项 A：URL 导入（最简单）

1. **打开 ApiPost** 应用
2. 点击左侧导航栏的 **"项目"**
3. 点击 **"新建项目"** 或选择现有项目
4. 点击项目右侧的 **"..."** 菜单
5. 选择 **"导入数据"**
6. 在弹出的对话框中选择 **"OpenAPI/Swagger"**
7. 选择 **"URL 导入"**
8. 输入 URL：`http://localhost:8001/openapi.json`
9. 点击 **"获取数据"**
10. 预览无误后，点击 **"确定导入"**

#### 选项 B：文件导入

1. **打开 ApiPost** 应用
2. 点击左侧导航栏的 **"项目"**
3. 点击项目右侧的 **"..."** 菜单
4. 选择 **"导入数据"**
5. 在弹出的对话框中选择 **"OpenAPI/Swagger"**
6. 选择 **"文件导入"**
7. 点击 **"选择文件"**，上传之前保存的 `knife_operator_api.json`
8. 点击 **"确定导入"**

### ✅ 步骤 4：验证导入结果

导入成功后，您应该能在 ApiPost 中看到以下接口分组：

#### 📁 刀头借出管理
- `GET /api/v1/lend-records` - 获取借出记录列表
- `POST /api/v1/lend-records` - 新增借出记录
- `PUT /api/v1/lend-records/{borrow_id}` - 更新借出记录
- `GET /api/v1/lend-records/{borrow_id}` - 获取借出记录详情
- `POST /api/v1/batch-return` - 批量归还刀头
- `POST /api/v1/return` - 归还刀头
- `POST /api/v1/temp-store` - 暂存刀头

#### 📁 刀头暂存管理
- `GET /api/v1/temp-store-records` - 获取刀头暂存记录列表
- `POST /api/v1/temp-store-records` - 新增刀柄暂存记录
- `POST /api/v1/temp-store-batch-return` - 暂存刀头批量归还

#### 📁 刀柄借出管理
- `GET /api/v1/handle/lend-records` - 获取刀柄借出记录列表
- `POST /api/v1/handle/lend-records` - 新增刀柄借出记录
- `PUT /api/v1/handle/lend-records/{handle_id}` - 更新刀柄借出记录
- `GET /api/v1/handle/lend-records/{handle_id}` - 获取刀柄借出记录详情
- `POST /api/v1/handle/batch-return` - 批量归还刀柄
- `POST /api/v1/handle/return` - 归还刀柄
- `POST /api/v1/handle/temp-store` - 暂存刀柄

#### 📁 刀柄暂存管理（核心功能）
- `GET /api/v1/handle/temp-store-records` - 获取刀柄暂存记录列表 ⭐
- `POST /api/v1/handle/temp-store-records` - 新增刀柄暂存记录 ⭐
- `PUT /api/v1/handle/temp-store/{record_id}` - 编辑刀柄暂存记录 ⭐
- `GET /api/v1/handle/temp-store/{record_id}` - 获取刀柄暂存记录详情 ⭐
- `POST /api/v1/handle/temp-store` - 创建刀柄暂存（从借出） ⭐
- `POST /api/v1/handle/return` - 归还刀柄暂存 ⭐
- `POST /api/v1/handle/temp-store-batch-return` - 批量归还刀柄暂存 ⭐

#### 📁 系统接口
- `GET /` - 服务根路径
- `GET /health` - 健康检查

---

## 方法二：使用 FastAPI 内置文档

FastAPI 提供了两个强大的内置交互式文档界面，可以直接在浏览器中查看和测试接口。

### 🎨 Swagger UI（推荐用于测试）

**访问地址**：
```
http://localhost:8001/docs
```

**功能特点**：
- ✅ 查看所有接口和参数说明
- ✅ **直接在线测试接口**（点击 "Try it out" 按钮）
- ✅ 查看请求和响应的数据模型
- ✅ 自动生成示例代码
- ✅ 支持认证配置
- ✅ 实时更新（代码修改后刷新即可）

**使用步骤**：
1. 访问 `http://localhost:8001/docs`
2. 找到要测试的接口
3. 点击接口展开详情
4. 点击 **"Try it out"** 按钮
5. 填写请求参数
6. 点击 **"Execute"** 执行请求
7. 查看响应结果

**截图示例**：
```
┌─────────────────────────────────────────┐
│  Swagger UI                              │
├─────────────────────────────────────────┤
│  刀柄暂存管理                             │
│  ├── GET  /api/v1/handle/temp-store... │
│  ├── POST /api/v1/handle/temp-store... │
│  ├── PUT  /api/v1/handle/temp-store/... │
│  └── ...                                │
└─────────────────────────────────────────┘
```

### 📖 ReDoc（推荐用于阅读文档）

**访问地址**：
```
http://localhost:8001/redoc
```

**功能特点**：
- ✅ 更美观的文档展示
- ✅ 更好的阅读体验
- ✅ 支持搜索功能
- ✅ 自动生成三栏式布局
- ✅ 支持打印和导出
- ✅ 响应式设计

**优点**：
- 文档结构清晰
- 适合生成PDF文档
- 适合培训和演示

---

## 优化后的功能

我已经优化了 `main.py` 文件，添加了更详细的 API 文档配置：

### ✨ 新增特性

#### 1. 详细的 API 描述
- 项目标题：**刀具管理系统 - 操作员接口**
- 详细的功能模块说明
- 接口规范说明
- 联系方式和许可证信息

#### 2. 接口标签分组
所有接口自动按功能模块分组：
- 刀头借出管理
- 刀头暂存管理
- 刀柄借出管理
- **刀柄暂存管理**（您最新实现的功能）
- 系统接口

#### 3. 增强的接口文档
每个接口都包含：
- 详细的功能描述
- 参数说明
- 响应示例
- 使用说明

---

## 在 ApiPost 中测试接口

### 测试步骤

1. **选择接口**
   - 在左侧接口列表中选择要测试的接口

2. **填写参数**
   - **Query 参数**：在 "Params" 标签页填写
   - **Body 参数**：在 "Body" 标签页选择 JSON 格式并填写
   - **Path 参数**：在 URL 路径中填写（如 `{record_id}` 替换为实际ID）

3. **发送请求**
   - 点击 **"发送"** 按钮
   - 查看响应结果

4. **保存测试用例**
   - 点击 **"保存为示例"**
   - 方便后续重复使用

### 示例：测试刀柄暂存详情接口

#### 接口信息
- **方法**：GET
- **路径**：`/api/v1/handle/temp-store/{record_id}`
- **基础URL**：`http://localhost:8001`

#### 在 ApiPost 中配置

1. **设置请求方法**：GET
2. **设置 URL**：`http://localhost:8001/api/v1/handle/temp-store/1`
3. **点击发送**
4. **查看响应**：
   ```json
   {
     "code": 200,
     "msg": "获取成功",
     "data": {
       "id": 1,
       "storageCode": "HTS2023001",
       "borrowerName": "张三",
       "storageUser": "zhangsan",
       "brandName": "品牌A",
       "handleSpec": "BT40-型号X",
       "quantity": 3,
       ...
     }
   }
   ```

---

## 环境变量配置（可选）

如果您需要配置不同的环境（开发、测试、生产），可以在 ApiPost 中设置环境变量：

### 创建环境

1. 点击 ApiPost 右上角的 **"环境"** 图标
2. 点击 **"新建环境"**
3. 命名为 "开发环境"
4. 添加变量：
   ```
   base_url = http://localhost:8001
   api_prefix = /api/v1
   ```
5. 保存

### 使用环境变量

在 URL 中使用：
```
{{base_url}}{{api_prefix}}/handle/temp-store/1
```

这样切换环境时只需要修改环境变量，不需要修改每个接口的 URL。

---

## 导出文档（可选）

### 从 ApiPost 导出

1. 选择项目
2. 点击 **"..."** 菜单
3. 选择 **"导出数据"**
4. 选择格式：
   - **Markdown**：生成文档
   - **HTML**：生成网页
   - **JSON**：OpenAPI 格式
   - **Postman**：Postman Collection

### 从 FastAPI 导出

**导出 OpenAPI JSON**：
```bash
curl http://localhost:8001/openapi.json > api_docs.json
```

**生成 Markdown 文档**（需要安装工具）：
```bash
# 安装 openapi-generator
npm install -g @openapitools/openapi-generator-cli

# 生成 Markdown 文档
openapi-generator-cli generate -i http://localhost:8001/openapi.json -g markdown -o ./docs
```

---

## 常见问题

### ❓ Q1: 导入后接口数量不对？

**A**: 
1. 确保服务正在运行（访问 `http://localhost:8001/docs` 验证）
2. 检查是否有接口报错导致未注册
3. 重新获取 openapi.json 文件
4. 在 ApiPost 中清除缓存后重新导入

### ❓ Q2: 接口分组混乱怎么办？

**A**: 
1. 确保已更新 `main.py` 文件（使用我优化后的版本）
2. 重启服务
3. 重新导入 openapi.json
4. 手动在 ApiPost 中调整分组

### ❓ Q3: 无法访问 http://localhost:8001/openapi.json？

**A**: 
1. 检查服务是否启动成功
2. 检查端口是否被占用：`lsof -ti:8001`
3. 尝试访问 `http://127.0.0.1:8001/openapi.json`
4. 检查防火墙设置

### ❓ Q4: 参数示例值不正确？

**A**: 
FastAPI 会根据 Pydantic 模型自动生成示例。如需自定义示例，可以在模型中使用 `Field` 的 `example` 参数：

```python
from pydantic import BaseModel, Field

class Example(BaseModel):
    name: str = Field(..., example="张三")
    age: int = Field(..., example=25)
```

### ❓ Q5: ApiPost 中测试接口返回 404？

**A**: 
1. 检查 URL 是否正确（包含 `/api/v1` 前缀）
2. 检查路径参数是否正确替换（如 `{record_id}` 改为实际数字）
3. 在 Swagger UI 中先测试确认接口可用
4. 检查 HTTP 方法是否正确（GET/POST/PUT）

### ❓ Q6: 如何更新已导入的接口？

**A**: 
1. 修改代码后重启服务
2. 重新访问 `http://localhost:8001/openapi.json`
3. 在 ApiPost 中再次导入（选择"覆盖"模式）
4. 或者手动修改 ApiPost 中的接口

---

## 最佳实践

### ✅ 建议的工作流程

1. **开发阶段**
   - 使用 Swagger UI (`/docs`) 边开发边测试
   - 实时查看接口文档
   - 快速验证功能

2. **联调阶段**
   - 导入到 ApiPost
   - 创建测试用例
   - 保存常用的请求参数
   - 与前端团队共享

3. **测试阶段**
   - 使用 ApiPost 的测试集功能
   - 批量执行测试用例
   - 导出测试报告

4. **文档阶段**
   - 使用 ReDoc (`/redoc`) 查看文档
   - 导出 OpenAPI JSON
   - 生成 Markdown 或 HTML 文档

### ✅ 团队协作建议

1. **共享 OpenAPI JSON**
   - 将 openapi.json 文件加入版本控制
   - 团队成员可直接导入

2. **使用 ApiPost 的团队功能**
   - 创建团队空间
   - 共享接口集合
   - 统一测试环境

3. **定期同步**
   - API 更新后及时重新导入
   - 通知团队成员更新

---

## 总结

### 🎯 推荐方案

**日常开发**：使用 FastAPI Swagger UI (`http://localhost:8001/docs`)
- ✅ 无需额外配置
- ✅ 实时更新
- ✅ 可直接测试

**团队协作**：导入到 ApiPost
- ✅ 保存测试用例
- ✅ 团队共享
- ✅ 批量测试

**对外文档**：使用 ReDoc (`http://localhost:8001/redoc`)
- ✅ 美观专业
- ✅ 适合演示
- ✅ 可导出PDF

### 📝 快速开始

```bash
# 1. 启动服务
python knife_operator/main.py

# 2. 浏览器访问（查看文档）
# http://localhost:8001/docs

# 3. 导入到 ApiPost（可选）
# 访问 http://localhost:8001/openapi.json
# 在 ApiPost 中导入该 URL
```

现在您就可以轻松地在 ApiPost 中管理和测试所有接口了！🎉

---

**文档版本**: v1.0  
**更新日期**: 2025-10-19  
**作者**: 开发团队
