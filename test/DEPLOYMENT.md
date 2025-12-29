# 部署指南

## 快速部署

### 1. 环境准备
```bash
# 确保Python 3.8+已安装
python --version

# 安装项目依赖
pip install flask pymysql numpy pandas
```

### 2. 数据库配置
1. 启动MySQL服务
2. 创建数据库：
```sql
CREATE DATABASE hunan_agriculture CHARACTER SET utf8mb4;
```
3. 修改 `config.py` 中的数据库配置

### 3. 启动应用
```bash
python app.py
```

### 4. 访问系统
打开浏览器访问：http://localhost:5004

## 生产环境部署

### 使用Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5004 app:app
```

### 使用Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5004
CMD ["python", "app.py"]
```

## 注意事项
- 确保MySQL服务正常运行
- 检查防火墙端口5004是否开放
- 生产环境建议使用HTTPS
- 定期备份数据库数据
