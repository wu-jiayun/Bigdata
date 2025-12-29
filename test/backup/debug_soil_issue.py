import requests
import json

try:
    # 初始化系统
    resp1 = requests.post('http://localhost:5004/api/system/initialize')
    init_result = resp1.json()
    print('初始化结果:', init_result)
    
    # 运行分析
    resp2 = requests.post('http://localhost:5004/api/analysis/run')
    analysis_result = resp2.json()
    print('分析结果:', analysis_result)
    
    # 检查土壤分析
    resp3 = requests.get('http://localhost:5004/api/echarts/soil_analysis')
    soil_result = resp3.json()
    print('土壤分析状态:', soil_result.get('status'))
    
    if soil_result.get('status') == 'success':
        charts = soil_result.get('charts', {})
        for name, chart in charts.items():
            print(f'图表: {name}')
            if 'data' in chart:
                print(f'  数据点数量: {len(chart["data"])}')
                if chart["data"]:
                    print(f'  示例数据: {chart["data"][0]}')
            elif 'xAxis' in chart:
                print(f'  X轴标签数量: {len(chart["xAxis"])}')
                if chart["xAxis"]:
                    print(f'  示例标签: {chart["xAxis"][:3]}')
            print()
    else:
        print('土壤分析错误:', soil_result.get('message'))
        
except Exception as e:
    print('请求失败:', str(e))
