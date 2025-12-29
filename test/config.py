# 湖南省农业分析系统配置文件

# Flask应用配置
class Config:
    # 基本配置
    DEBUG = True
    SECRET_KEY = 'hunan-agriculture-analysis-system-2025'
    
    # 服务器配置
    HOST = '0.0.0.0'
    PORT = 5004
    
    # 数据库配置
    MYSQL_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': 'your_password',  # 请修改为实际密码
        'database': 'hunan_agriculture',
        'charset': 'utf8mb4',
        'autocommit': True
    }
    
    # Spark配置
    SPARK_CONFIG = {
        'app_name': '湖南省农业分析系统',
        'master': 'local[*]',
        'memory': '4g',
        'cores': 4
    }
    
    # 缓存配置
    CACHE_TIMEOUT = 300  # 5分钟缓存
    
    # 日志配置
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

# 开发环境配置
class DevelopmentConfig(Config):
    DEBUG = True
    
# 生产环境配置
class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = 'WARNING'

# 默认配置
config = DevelopmentConfig
