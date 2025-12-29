import requests
import json

try:
    # 获取土壤分析数据
    resp = requests.get('http://localhost:5004/api/echarts/soil_analysis')
    result = resp.json()
    
    print("土壤分析API响应:")
    print("状态:", result.get('status'))
    
    if result.get('status') == 'success':
        charts = result.get('charts', {})
        print("可用图表:", list(charts.keys()))
        
        for chart_name, chart_data in charts.items():
            print(f"\n=== {chart_name} ===")
            print("标题:", chart_data.get('title', '无标题'))
            
            if 'data' in chart_data:
                data_len = len(chart_data['data'])
                print(f"数据点数量: {data_len}")
                if data_len > 0:
                    print("前2个数据点:", chart_data['data'][:2])
            
            if 'xAxis' in chart_data:
                x_len = len(chart_data['xAxis'])
                print(f"X轴数据长度: {x_len}")
                if x_len > 0:
                    print("前3个X轴标签:", chart_data['xAxis'][:3])
            
            if 'series' in chart_data:
                series_len = len(chart_data['series'])
                print(f"数据系列数量: {series_len}")
                if series_len > 0:
                    first_series = chart_data['series'][0]
                    if 'data' in first_series:
                        print(f"第一个系列数据长度: {len(first_series['data'])}")
    else:
        print("错误信息:", result.get('message'))
        
except Exception as e:
    print("请求失败:", str(e))
