# 湖南省农业种植适宜性区划分析系统 - 项目结构

## 📁 项目目录结构

```
d:\bishe\test/
├── app.py                          # 主应用程序文件
├── config.py                       # 配置文件
├── requirements.txt                 # Python依赖包
├── README.md                       # 项目说明文档
├── PROJECT_STRUCTURE.md            # 项目结构说明（本文件）
├── 
├── templates/                      # HTML模板文件
│   ├── index.html                  # 主页面
│   ├── main_dashboard.html         # 主仪表板
│   ├── zoning_distribution.html    # 多准则适宜性区划
│   ├── report_generator.html       # 联网报告生成
│   ├── suitability_evaluation.html # 适宜性评价
│   ├── zoning_analysis.html        # 区划分析
│   ├── temperature_analysis.html   # 温度分析
│   ├── soil_analysis.html          # 土壤分析
│   ├── crop_analysis.html          # 作物分析
│   ├── login.html                  # 登录页面
│   ├── spark_agricultural_index.html # Spark农业指数
│   └── components/                 # 组件目录
│       ├── header.html
│       ├── footer.html
│       ├── sidebar.html
│       └── charts.html
│
├── static/                         # 静态资源文件
│   ├── css/                        # 样式文件
│   │   └── style.css
│   ├── js/                         # JavaScript文件
│   │   ├── charts.js
│   │   ├── dashboard.js
│   │   ├── echarts.min.js
│   │   ├── jquery.min.js
│   │   ├── main.js
│   │   ├── reports.js
│   │   └── zoning.js
│   └── hunan.json                  # 湖南省地图数据
│
├── utils/                          # 工具模块
│   └── database_connector.py       # 数据库连接器
│
├── docs/                           # 文档目录
│   ├── API.md
│   ├── DEPLOYMENT.md
│   ├── FEATURES.md
│   ├── INSTALLATION.md
│   └── USER_GUIDE.md
│
└── backup/                         # 备份文件（开发过程中的备份）
```

## 🎯 核心功能模块

### 1. 主应用程序 (app.py)
- **系统初始化**: MySQL数据库连接和Spark系统初始化
- **数据分析API**: 温度、土壤、作物分析接口
- **区划分析**: 多准则适宜性区划算法
- **联网报告生成**: 实时数据获取和报告生成
- **数据导出**: 纯文本格式完整数据导出

### 2. 前端模板系统
- **响应式设计**: 基于Bootstrap 5的现代化界面
- **交互式图表**: ECharts图表库集成
- **实时数据展示**: 联网数据可视化
- **报告预览**: 完整数据预览和下载

### 3. 数据处理模块
- **数据库连接**: MySQL数据库操作
- **实时数据获取**: 模拟联网API数据获取
- **数据分析**: 多准则评价和区划算法
- **报告生成**: 智能报告内容生成

## 🔧 技术栈

### 后端技术
- **Python 3.x**: 主要编程语言
- **Flask**: Web框架
- **pandas**: 数据处理
- **pymysql**: MySQL数据库连接

### 前端技术
- **HTML5/CSS3**: 页面结构和样式
- **JavaScript**: 交互逻辑
- **Bootstrap 5**: UI框架
- **ECharts**: 图表库
- **jQuery**: DOM操作

### 数据存储
- **MySQL**: 主数据库
- **JSON**: 地图数据存储
- **文本文件**: 报告导出格式

## 📊 主要功能

1. **多准则适宜性区划**
   - 支持12种农作物类型
   - 县级、乡镇级、村级精度
   - 湖南省地图可视化

2. **联网报告生成**
   - 实时市场行情数据
   - 天气预报集成
   - 政策动态分析
   - 技术趋势跟踪

3. **数据分析与可视化**
   - 温度趋势分析
   - 土壤分布分析
   - 作物适宜性评价
   - 交互式图表展示

4. **报告导出功能**
   - 完整数据导出
   - 纯文本格式
   - 包含联网数据
   - 县市详情数据

## 🚀 部署说明

1. **环境要求**
   - Python 3.7+
   - MySQL 5.7+
   - 现代浏览器支持

2. **安装步骤**
   ```bash
   pip install -r requirements.txt
   python app.py
   ```

3. **访问地址**
   - 本地访问: http://localhost:5004
   - 系统支持局域网访问

## 📝 开发规范

- 代码注释完整
- 函数命名规范
- 错误处理完善
- 日志记录详细
- 响应式设计
- 用户体验优化
