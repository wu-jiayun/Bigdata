import requests
import json

try:
    resp = requests.get('http://localhost:5004/api/echarts/crop_suitability')
    result = resp.json()
    
    print('作物API状态:', result.get('status'))
    
    if result.get('status') == 'success':
        charts = result.get('charts', {})
        for name, chart in charts.items():
            print(f'\n=== {name} ===')
            print(f'类型: {type(chart)}')
            if isinstance(chart, dict):
                print(f'键: {list(chart.keys())}')
                for key, value in chart.items():
                    if isinstance(value, (str, int, float, bool)):
                        print(f'  {key}: {type(value)} - {value}')
                    elif isinstance(value, list):
                        print(f'  {key}: {type(value)} - 长度 {len(value)}')
                        if value and len(value) > 0:
                            print(f'    示例: {value[0]}')
                    elif isinstance(value, dict):
                        print(f'  {key}: {type(value)} - 键 {list(value.keys()) if value else "空字典"}')
                    else:
                        print(f'  {key}: {type(value)} - {value}')
    else:
        print('错误:', result.get('message'))
    
except Exception as e:
    print('检查失败:', e)
