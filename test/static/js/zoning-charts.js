/**
 * 沃土规划师 - 区划图表模块
 * 包含区划优化建议相关的图表加载功能
 */

/**
 * 加载区划图表
 */
async function loadZoningCharts() {
    try {
        console.log('🗺️ 开始加载区划图表...');
        
        // 检查SparkCore是否存在
        if (!window.SparkCore || !window.SparkCore.charts) {
            console.error('❌ SparkCore.charts 未初始化');
            return;
        }
        
        const charts = window.SparkCore.charts;
        console.log('🔍 检查区划图表容器:', {
            zoningScatterChart: !!charts.zoningScatterChart,
            optimizationMapChart: !!charts.optimizationMapChart
        });
        
        const response = await fetch('/api/echarts/zoning_optimization');
        const result = await response.json();
        
        console.log('📊 区划分析API响应:', result);
        
        if (result.status === 'success') {
            const charts_data = result.charts;
            console.log('📈 区划图表数据:', Object.keys(charts_data));
            
            // 区划散点图（县市土壤质量分布）
            if (charts_data.zoning_scatter && charts_data.zoning_scatter.series && charts.zoningScatterChart) {
                console.log('📊 设置区划散点图');
                charts.zoningScatterChart.setOption({
                    title: { 
                        text: charts_data.zoning_scatter.title || '湖南省县市土壤质量分布',
                        left: 'center',
                        textStyle: { fontSize: 16, fontWeight: 'bold' }
                    },
                    tooltip: { 
                        trigger: 'item',
                        formatter: function(params) {
                            return `${params.data[2]}<br/>pH值: ${params.data[0]}<br/>质量评分: ${params.data[1]}<br/>样本数: ${params.data[3]}`;
                        }
                    },
                    xAxis: { 
                        type: 'value', 
                        name: 'pH值',
                        nameLocation: 'middle',
                        nameGap: 30
                    },
                    yAxis: { 
                        type: 'value', 
                        name: '土壤质量评分',
                        nameLocation: 'middle',
                        nameGap: 50
                    },
                    series: charts_data.zoning_scatter.series.map(s => ({
                        ...s,
                        itemStyle: {
                            color: '#4ECDC4',
                            borderColor: '#333',
                            borderWidth: 1
                        },
                        emphasis: {
                            itemStyle: {
                                color: '#FF6B6B'
                            }
                        }
                    }))
                });
                console.log('✅ 区划散点图设置完成');
            }
            
            // 优化建议图表（简化为柱状图，避免地图组件问题）
            if (charts_data.optimization_map && charts_data.optimization_map.series && charts.optimizationMapChart) {
                console.log('📊 设置优化建议图表');
                
                // 提取地理数据转换为柱状图
                const mapData = charts_data.optimization_map.series[0].data || [];
                const cityNames = mapData.map(item => item[2] || '未知城市');
                const cityValues = mapData.map((item, index) => index + 1); // 简单的排序值
                
                charts.optimizationMapChart.setOption({
                    title: { 
                        text: '湖南省优化建议区域',
                        left: 'center',
                        textStyle: { fontSize: 16, fontWeight: 'bold' }
                    },
                    tooltip: { 
                        trigger: 'axis',
                        axisPointer: { type: 'shadow' }
                    },
                    xAxis: { 
                        type: 'category',
                        data: cityNames,
                        axisLabel: { 
                            rotate: 45,
                            fontSize: 12
                        }
                    },
                    yAxis: { 
                        type: 'value', 
                        name: '优化优先级',
                        nameLocation: 'middle',
                        nameGap: 50
                    },
                    series: [{
                        name: '优化建议',
                        type: 'bar',
                        data: cityValues,
                        itemStyle: {
                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                {offset: 0, color: '#83bff6'},
                                {offset: 0.5, color: '#188df0'},
                                {offset: 1, color: '#188df0'}
                            ])
                        },
                        emphasis: {
                            itemStyle: {
                                color: '#FF6B6B'
                            }
                        }
                    }]
                });
                console.log('✅ 优化建议图表设置完成');
            }
            
            console.log('✅ 区划图表加载完成');
        } else {
            console.error('区划分析API返回错误:', result.message);
        }
    } catch (error) {
        console.error('加载区划图表失败:', error);
    }
}

// 将区划图表功能添加到ChartLoader
if (window.ChartLoader) {
    window.ChartLoader.loadZoningCharts = loadZoningCharts;
} else {
    window.ChartLoader = { loadZoningCharts };
}
