/**
 * 沃土规划师 - 图表加载模块
 * 包含所有图表的加载和渲染功能
 */

/**
 * 加载所有图表
 */
async function loadAllCharts() {
    console.log('🚀 开始加载所有图表...');
    try {
        await loadClimateCharts();
        console.log('✅ 气候图表加载完成');
        
        await loadSoilCharts();
        console.log('✅ 土壤图表加载完成');
        
        await loadCropCharts();
        console.log('✅ 作物图表加载完成');
        
        await loadZoningCharts();
        console.log('✅ 区划图表加载完成');
        
        console.log('🎉 所有图表加载完成');
    } catch (error) {
        console.error('❌ 图表加载失败:', error);
        throw error;
    }
}

/**
 * 加载气候图表
 */
async function loadClimateCharts() {
    try {
        console.log('🌡️ 开始加载气候图表...');
        const response = await fetch('/api/echarts/climate_trends');
        const result = await response.json();
        
        console.log('📊 气候分析API响应:', result);
        
        if (result.status === 'success') {
            const charts_data = result.charts;
            console.log('📈 气候图表数据:', Object.keys(charts_data));
            
            // 温度趋势图
            if (charts_data.temperature_trend && window.SparkCore.charts.tempTrendChart) {
                console.log('📈 设置温度趋势图');
                window.SparkCore.charts.tempTrendChart.setOption({
                    title: { 
                        text: charts_data.temperature_trend.title || '湖南省月度温度变化趋势',
                        left: 'center',
                        textStyle: { fontSize: 16, fontWeight: 'bold' }
                    },
                    tooltip: { 
                        trigger: 'axis',
                        formatter: '{a}<br/>{b}: {c}°C'
                    },
                    legend: { 
                        data: charts_data.temperature_trend.series.map(s => s.name),
                        top: 'bottom'
                    },
                    xAxis: { 
                        type: 'category',
                        data: charts_data.temperature_trend.xAxis,
                        axisLabel: { fontSize: 12 }
                    },
                    yAxis: { 
                        type: 'value', 
                        name: '温度(°C)',
                        nameTextStyle: { fontSize: 12 }
                    },
                    series: charts_data.temperature_trend.series.map(s => ({
                        ...s,
                        smooth: true,
                        lineStyle: { width: 3 },
                        itemStyle: { 
                            color: s.name.includes('平均') ? '#FF6B6B' : '#4ECDC4'
                        }
                    }))
                });
                console.log('✅ 温度趋势图设置完成');
            }
            
            // 年度趋势图
            if (charts_data.annual_trend && window.SparkCore.charts.precipPatternChart) {
                console.log('📈 设置年度趋势图');
                window.SparkCore.charts.precipPatternChart.setOption({
                    title: { 
                        text: charts_data.annual_trend.title || '年度温度趋势',
                        left: 'center',
                        textStyle: { fontSize: 16, fontWeight: 'bold' }
                    },
                    tooltip: { 
                        trigger: 'axis',
                        formatter: '{a}<br/>{b}: {c}°C'
                    },
                    legend: { 
                        data: charts_data.annual_trend.series ? charts_data.annual_trend.series.map(s => s.name) : [],
                        top: 'bottom'
                    },
                    xAxis: { 
                        type: 'category',
                        data: charts_data.annual_trend.xAxis || [],
                        axisLabel: { fontSize: 12 }
                    },
                    yAxis: { 
                        type: 'value', 
                        name: '温度(°C)',
                        nameTextStyle: { fontSize: 12 }
                    },
                    series: charts_data.annual_trend.series || []
                });
                console.log('✅ 年度趋势图设置完成');
            }
            
            // 季节对比图
            if (charts_data.seasonal_comparison && window.SparkCore.charts.climateHeatmapChart) {
                console.log('🌡️ 设置季节对比图');
                window.SparkCore.charts.climateHeatmapChart.setOption({
                    title: { 
                        text: '湖南省季节温度对比',
                        left: 'center',
                        textStyle: { fontSize: 16, fontWeight: 'bold' }
                    },
                    tooltip: { 
                        trigger: 'item',
                        formatter: '{a} <br/>{b}: {c}°C ({d}%)'
                    },
                    legend: { 
                        orient: 'vertical', 
                        left: 'left',
                        top: 'middle'
                    },
                    series: [{
                        name: '季节温度',
                        type: 'pie',
                        radius: '60%',
                        data: charts_data.seasonal_comparison.data || [],
                        emphasis: { 
                            itemStyle: { 
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        },
                        label: {
                            show: true,
                            formatter: '{b}: {c}°C'
                        }
                    }]
                });
                console.log('✅ 季节对比图设置完成');
            }
            
            console.log('✅ 气候图表加载完成');
        } else {
            console.error('气候分析API返回错误:', result.message);
        }
    } catch (error) {
        console.error('加载气候图表失败:', error);
    }
}

// 导出图表加载功能
window.ChartLoader = {
    loadAllCharts,
    loadClimateCharts
};
