# 安装部署指南

## 系统要求

### 硬件要求
- **CPU**: 4核心以上（推荐8核心）
- **内存**: 8GB以上（推荐16GB）
- **存储**: 20GB可用空间
- **网络**: 稳定的网络连接

### 软件要求
- **操作系统**: Windows 10/11, Linux, macOS
- **Python**: 3.8或更高版本
- **MySQL**: 5.7或更高版本
- **浏览器**: Chrome 90+, Firefox 88+, Safari 14+

## 安装步骤

### 1. 环境准备

#### 安装Python
```bash
# Windows
下载Python 3.8+安装包并安装
https://www.python.org/downloads/

# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install python3 python3-pip

# macOS
brew install python3
```

#### 安装MySQL
```bash
# Windows
下载MySQL安装包并安装
https://dev.mysql.com/downloads/mysql/

# Linux (Ubuntu/Debian)
sudo apt install mysql-server

# macOS
brew install mysql
```

### 2. 项目部署

#### 下载项目
```bash
git clone [项目地址]
cd 湖南农业分析系统
```

#### 安装Python依赖
```bash
pip install -r requirements.txt
```

#### 配置数据库
1. 启动MySQL服务
2. 创建数据库：
```sql
CREATE DATABASE hunan_agriculture CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. 修改配置文件 `config.py`：
```python
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',      # 修改为您的MySQL用户名
    'password': 'your_password',  # 修改为您的MySQL密码
    'database': 'hunan_agriculture',
    'charset': 'utf8mb4',
    'autocommit': True
}
```

### 3. 启动应用

#### 开发环境启动
```bash
python app.py
```

#### 生产环境启动
```bash
# 使用gunicorn（推荐）
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5004 app:app

# 或使用uwsgi
pip install uwsgi
uwsgi --http :5004 --wsgi-file app.py --callable app
```

### 4. 访问系统

打开浏览器访问：
- 开发环境：http://localhost:5004
- 生产环境：http://your-server-ip:5004

## 配置说明

### 数据库配置
在 `utils/database_connector.py` 中配置MySQL连接信息：
```python
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'hunan_agriculture',
    'charset': 'utf8mb4'
}
```

### 端口配置
在 `app.py` 中修改端口：
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
```

## 故障排除

### 常见问题

#### 1. 数据库连接失败
```
错误：Can't connect to MySQL server
解决：
- 检查MySQL服务是否启动
- 验证用户名和密码
- 确认数据库名称正确
```

#### 2. 端口被占用
```
错误：Address already in use
解决：
- 更改端口号
- 或终止占用端口的进程
```

#### 3. 模块导入错误
```
错误：ModuleNotFoundError
解决：
- 检查Python版本
- 重新安装依赖包：pip install -r requirements.txt
```

#### 4. 图表不显示
```
问题：ECharts图表无法加载
解决：
- 检查网络连接
- 清除浏览器缓存
- 确保JavaScript已启用
```

### 性能优化

#### 数据库优化
```sql
-- 为常用查询添加索引
CREATE INDEX idx_temperature_date ON temperature_data(date);
CREATE INDEX idx_soil_type ON soil_data(soil_type);
```

#### 应用优化
- 启用数据缓存
- 使用CDN加速静态资源
- 配置反向代理（Nginx）

## 安全配置

### 生产环境安全
1. 修改默认密码
2. 启用HTTPS
3. 配置防火墙
4. 定期备份数据

### 访问控制
```python
# 在app.py中添加IP白名单
ALLOWED_IPS = ['127.0.0.1', '192.168.1.0/24']
```

## 监控和日志

### 日志配置
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### 性能监控
- 使用系统监控工具监控CPU、内存使用
- 监控数据库连接数和查询性能
- 设置告警机制

## 备份和恢复

### 数据备份
```bash
# 备份数据库
mysqldump -u username -p hunan_agriculture > backup.sql

# 恢复数据库
mysql -u username -p hunan_agriculture < backup.sql
```

### 应用备份
```bash
# 备份应用文件
tar -czf app-backup-$(date +%Y%m%d).tar.gz /path/to/app
```
