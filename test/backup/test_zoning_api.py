import requests

try:
    # 测试区划API
    resp = requests.get('http://localhost:5004/api/echarts/zoning_optimization')
    print('区划API状态码:', resp.status_code)
    
    if resp.status_code == 200:
        result = resp.json()
        print('区划API状态:', result.get('status'))
        if result.get('status') == 'success':
            charts = result.get('charts', {})
            print('区划图表数据:', list(charts.keys()))
            for name, chart in charts.items():
                print(f'{name}: {chart.get("title", "无标题")}')
                if 'series' in chart:
                    print(f'  系列数量: {len(chart["series"])}')
                if 'data' in chart:
                    print(f'  数据点数量: {len(chart["data"])}')
        else:
            print('错误信息:', result.get('message'))
    else:
        print('HTTP错误:', resp.text[:200])
        
except Exception as e:
    print('测试失败:', e)
