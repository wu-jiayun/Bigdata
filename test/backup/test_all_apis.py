import requests
import json

try:
    # 测试系统初始化
    print('1. 测试系统初始化...')
    resp1 = requests.post('http://localhost:5004/api/system/initialize')
    result1 = resp1.json()
    print('初始化状态:', result1.get('status'))
    
    if result1.get('status') == 'success':
        print('数据摘要:', result1.get('data_summary'))
        
        # 测试分析运行
        print('\n2. 测试分析运行...')
        resp2 = requests.post('http://localhost:5004/api/analysis/run')
        result2 = resp2.json()
        print('分析状态:', result2.get('status'))
        
        if result2.get('status') == 'success':
            # 测试各个图表API
            apis = [
                '/api/echarts/climate_trends',
                '/api/echarts/soil_analysis', 
                '/api/echarts/crop_suitability',
                '/api/echarts/zoning_optimization'
            ]
            
            print('\n3. 测试图表API...')
            for api in apis:
                try:
                    resp = requests.get(f'http://localhost:5004{api}')
                    result = resp.json()
                    print(f'{api}: {result.get("status")}')
                    if result.get('status') == 'success':
                        charts = result.get('charts', {})
                        print(f'  图表数量: {len(charts)}')
                        for chart_name in charts.keys():
                            print(f'    - {chart_name}')
                    else:
                        print(f'  错误: {result.get("message")}')
                except Exception as e:
                    print(f'{api}: 请求失败 - {e}')
        else:
            print('分析失败:', result2.get('message'))
    else:
        print('初始化失败:', result1.get('message'))
        
except Exception as e:
    print('测试失败:', e)
