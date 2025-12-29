# API接口文档

## 概述

本系统提供RESTful API接口，支持农业数据的查询和分析功能。所有接口返回JSON格式数据。

## 基础信息

- **基础URL**: `http://localhost:5004`
- **数据格式**: JSON
- **字符编码**: UTF-8
- **HTTP方法**: GET, POST

## 系统管理接口

### 1. 系统初始化

**接口地址**: `POST /api/system/initialize`

**功能描述**: 初始化Spark系统，连接MySQL数据库

**请求参数**: 无

**响应示例**:
```json
{
    "status": "success",
    "message": "系统初始化成功",
    "data_summary": {
        "crop_types": 61,
        "precipitation_records": 316517,
        "soil_records": 2917,
        "temperature_records": 105
    },
    "processing_time": 2.34
}
```

### 2. 运行分析

**接口地址**: `POST /api/analysis/run`

**功能描述**: 运行综合农业数据分析

**请求参数**: 无

**响应示例**:
```json
{
    "status": "success",
    "message": "分析完成",
    "analysis_results": {
        "climate_analysis": "completed",
        "soil_analysis": "completed",
        "crop_analysis": "completed",
        "zoning_analysis": "completed"
    },
    "processing_time": 45.67
}
```

## 数据查询接口

### 3. 气候趋势数据

**接口地址**: `GET /api/echarts/climate_trends`

**功能描述**: 获取气候趋势分析的ECharts图表数据

**响应示例**:
```json
{
    "status": "success",
    "charts": {
        "temperature_trend": {
            "title": "月度温度变化趋势",
            "xAxis": ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
            "series": [
                {
                    "name": "平均温度",
                    "type": "line",
                    "data": [4.2, 7.1, 12.3, 18.7, 23.4, 27.8, 30.1, 29.3, 25.6, 19.8, 13.2, 7.5]
                }
            ]
        },
        "annual_trend": {
            "title": "年度温度趋势",
            "xAxis": ["2019", "2020", "2021", "2022", "2023"],
            "series": [
                {
                    "name": "年平均温度",
                    "type": "line",
                    "data": [17.2, 17.8, 17.1, 18.0, 17.6]
                }
            ]
        },
        "seasonal_comparison": {
            "title": "季节温度对比",
            "data": [
                {"name": "春季", "value": 15.8},
                {"name": "夏季", "value": 28.7},
                {"name": "秋季", "value": 19.5},
                {"name": "冬季", "value": 6.3}
            ]
        }
    }
}
```

### 4. 土壤分析数据

**接口地址**: `GET /api/echarts/soil_analysis`

**功能描述**: 获取土壤分析的ECharts图表数据

**响应示例**:
```json
{
    "status": "success",
    "charts": {
        "soil_type_pie": {
            "title": "土壤类型分布",
            "data": [
                {"name": "红壤", "value": 1245},
                {"name": "黄壤", "value": 856},
                {"name": "水稻土", "value": 623},
                {"name": "紫色土", "value": 193}
            ]
        },
        "ph_distribution": {
            "title": "pH值分布",
            "xAxis": ["强酸性", "酸性", "微酸性", "中性", "碱性"],
            "series": [
                {
                    "name": "样本数量",
                    "type": "bar",
                    "data": [234, 1456, 892, 267, 68]
                }
            ]
        },
        "county_quality_ranking": {
            "title": "县市土壤质量排名",
            "xAxis": ["长沙县", "浏阳市", "宁乡市", "望城区", "芙蓉区"],
            "series": [
                {
                    "name": "质量评分",
                    "type": "bar",
                    "data": [85.6, 82.3, 79.8, 77.2, 74.5]
                }
            ]
        }
    }
}
```

### 5. 作物适宜性数据

**接口地址**: `GET /api/echarts/crop_suitability`

**功能描述**: 获取作物适宜性分析的ECharts图表数据

**响应示例**:
```json
{
    "status": "success",
    "charts": {
        "suitability_distribution": {
            "title": "作物分类分布",
            "data": [
                {"name": "粮食作物", "value": 23},
                {"name": "经济作物", "value": 15},
                {"name": "蔬菜作物", "value": 12},
                {"name": "果树作物", "value": 8},
                {"name": "饲料作物", "value": 3}
            ]
        },
        "crop_advantages_radar": {
            "title": "作物温度需求",
            "xAxis": ["水稻", "玉米", "大豆", "棉花", "油菜"],
            "series": [
                {
                    "name": "最低温度",
                    "type": "bar",
                    "data": [12, 10, 8, 15, 5]
                },
                {
                    "name": "最高温度",
                    "type": "bar",
                    "data": [35, 32, 30, 38, 25]
                }
            ]
        },
        "limiting_factors_pie": {
            "title": "作物pH适应性",
            "data": [
                {"name": "酸性适应", "value": 28},
                {"name": "中性适应", "value": 25},
                {"name": "碱性适应", "value": 8}
            ]
        }
    }
}
```

### 6. 区划优化数据

**接口地址**: `GET /api/echarts/zoning_optimization`

**功能描述**: 获取区划优化建议的ECharts图表数据

**响应示例**:
```json
{
    "status": "success",
    "charts": {
        "zoning_scatter": {
            "title": "区划优化分布",
            "series": [
                {
                    "name": "县市分布",
                    "type": "scatter",
                    "data": [
                        [6.2, 78.5, "长沙县", 156],
                        [6.8, 82.3, "浏阳市", 234],
                        [5.9, 75.2, "宁乡市", 189]
                    ]
                }
            ]
        },
        "optimization_map": {
            "title": "最佳种植区域",
            "series": [
                {
                    "name": "优化建议",
                    "type": "map",
                    "data": [
                        [6.2, 78.5, "长沙县"],
                        [6.8, 82.3, "浏阳市"],
                        [5.9, 75.2, "宁乡市"]
                    ]
                }
            ]
        }
    }
}
```

## 错误响应

### 错误格式
```json
{
    "status": "error",
    "message": "错误描述",
    "error_code": "ERROR_CODE",
    "details": "详细错误信息"
}
```

### 常见错误码

| 错误码 | 描述 | 解决方案 |
|--------|------|----------|
| DB_CONNECTION_ERROR | 数据库连接失败 | 检查数据库配置和服务状态 |
| SPARK_INIT_ERROR | Spark初始化失败 | 检查Spark配置和资源 |
| DATA_NOT_FOUND | 数据未找到 | 确保数据已正确导入 |
| ANALYSIS_TIMEOUT | 分析超时 | 增加超时时间或优化查询 |
| INVALID_REQUEST | 无效请求 | 检查请求格式和参数 |

## 状态码说明

| HTTP状态码 | 说明 |
|------------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 500 | 服务器内部错误 |
| 503 | 服务不可用 |

## 使用示例

### JavaScript示例
```javascript
// 初始化系统
async function initializeSystem() {
    try {
        const response = await fetch('/api/system/initialize', {
            method: 'POST'
        });
        const result = await response.json();
        
        if (result.status === 'success') {
            console.log('初始化成功:', result.data_summary);
        } else {
            console.error('初始化失败:', result.message);
        }
    } catch (error) {
        console.error('请求失败:', error);
    }
}

// 获取气候数据
async function getClimateData() {
    try {
        const response = await fetch('/api/echarts/climate_trends');
        const result = await response.json();
        
        if (result.status === 'success') {
            // 处理图表数据
            const chartData = result.charts;
            console.log('气候数据:', chartData);
        }
    } catch (error) {
        console.error('获取数据失败:', error);
    }
}
```

### Python示例
```python
import requests
import json

# 基础URL
BASE_URL = 'http://localhost:5004'

# 初始化系统
def initialize_system():
    response = requests.post(f'{BASE_URL}/api/system/initialize')
    result = response.json()
    
    if result['status'] == 'success':
        print('初始化成功:', result['data_summary'])
        return True
    else:
        print('初始化失败:', result['message'])
        return False

# 获取气候数据
def get_climate_data():
    response = requests.get(f'{BASE_URL}/api/echarts/climate_trends')
    result = response.json()
    
    if result['status'] == 'success':
        return result['charts']
    else:
        print('获取数据失败:', result['message'])
        return None

# 使用示例
if __name__ == '__main__':
    if initialize_system():
        climate_data = get_climate_data()
        if climate_data:
            print('气候数据获取成功')
```

## 性能说明

### 响应时间
- **系统初始化**: 2-5秒
- **数据分析**: 30-60秒
- **数据查询**: 0.1-1秒

### 并发限制
- **最大并发**: 10个请求
- **超时时间**: 60秒
- **缓存时间**: 5分钟

### 数据更新
- **实时数据**: 无缓存
- **分析结果**: 5分钟缓存
- **基础数据**: 1小时缓存

---

**API版本**: v1.0.0  
**最后更新**: 2025年12月
