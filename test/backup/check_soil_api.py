import requests
import json

try:
    # 先初始化系统
    init_resp = requests.post('http://localhost:5004/api/system/initialize')
    print('初始化:', init_resp.json())
    
    # 运行分析
    analysis_resp = requests.post('http://localhost:5004/api/analysis/run')
    print('分析:', analysis_resp.json())
    
    # 检查土壤API
    soil_resp = requests.get('http://localhost:5004/api/echarts/soil_analysis')
    result = soil_resp.json()
    
    print('土壤API状态:', result.get('status'))
    
    if result.get('status') == 'success':
        charts = result.get('charts', {})
        for name, chart in charts.items():
            print(f'\n{name}:')
            if 'data' in chart:
                print(f'  数据项数: {len(chart["data"])}')
                if chart["data"]:
                    print(f'  示例数据: {chart["data"][0]}')
            if 'xAxis' in chart:
                print(f'  X轴项数: {len(chart["xAxis"])}')
                if chart["xAxis"]:
                    print(f'  X轴示例: {chart["xAxis"][:2]}')
            if 'series' in chart:
                print(f'  系列数: {len(chart["series"])}')
                if chart["series"]:
                    series = chart["series"][0]
                    if 'data' in series:
                        print(f'  系列数据: {len(series["data"])} 项')
    else:
        print('API错误:', result.get('message'))
        
except Exception as e:
    print('请求失败:', str(e))
