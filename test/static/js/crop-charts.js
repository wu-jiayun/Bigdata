/**
 * 沃土规划师 - 作物图表模块
 * 包含作物适宜性分析相关的图表加载功能
 */

/**
 * 加载作物图表
 */
async function loadCropCharts() {
    try {
        console.log('🌾 开始加载作物图表...');
        
        // 检查图表容器是否存在
        if (!window.SparkCore || !window.SparkCore.charts) {
            console.error('❌ SparkCore.charts 未初始化');
            return;
        }
        
        const charts = window.SparkCore.charts;
        console.log('🔍 检查作物图表容器:', {
            suitabilityDistChart: !!charts.suitabilityDistChart,
            cropRadarChart: !!charts.cropRadarChart,
            limitingFactorsChart: !!charts.limitingFactorsChart
        });
        
        const response = await fetch('/api/echarts/crop_suitability');
        const result = await response.json();
        
        console.log('📊 作物分析API响应:', result);
        
        if (result.status === 'success') {
            const charts_data = result.charts;
            console.log('📈 作物图表数据:', Object.keys(charts_data));
            
            // 作物分类分布饼图
            if (charts_data.suitability_distribution && charts_data.suitability_distribution.data && charts.suitabilityDistChart) {
                console.log('🥧 设置作物分类饼图，数据点:', charts_data.suitability_distribution.data.length);
                charts.suitabilityDistChart.setOption({
                    title: { 
                        text: charts_data.suitability_distribution.title || '湖南省作物分类分布',
                        left: 'center',
                        textStyle: { fontSize: 16, fontWeight: 'bold' }
                    },
                    tooltip: { 
                        trigger: 'item',
                        formatter: '{a} <br/>{b}: {c}种 ({d}%)'
                    },
                    legend: { 
                        orient: 'vertical', 
                        left: 'left',
                        top: 'middle'
                    },
                    series: [{
                        name: '作物分类',
                        type: 'pie',
                        radius: '60%',
                        data: charts_data.suitability_distribution.data,
                        emphasis: { 
                            itemStyle: { 
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        },
                        label: {
                            show: true,
                            formatter: '{b}: {c}种'
                        }
                    }]
                });
                console.log('✅ 作物分类饼图设置完成');
            }
            
            // 作物温度需求柱状图（原本是雷达图）
            if (charts_data.crop_advantages_radar && charts_data.crop_advantages_radar.xAxis && charts.cropRadarChart) {
                console.log('📊 设置作物温度需求图，作物数量:', charts_data.crop_advantages_radar.xAxis.length);
                charts.cropRadarChart.setOption({
                    title: { 
                        text: charts_data.crop_advantages_radar.title || '作物温度需求范围',
                        left: 'center',
                        textStyle: { fontSize: 16, fontWeight: 'bold' }
                    },
                    tooltip: { 
                        trigger: 'axis',
                        axisPointer: { type: 'shadow' }
                    },
                    legend: {
                        data: charts_data.crop_advantages_radar.series.map(s => s.name),
                        top: 'bottom'
                    },
                    xAxis: { 
                        type: 'category',
                        data: charts_data.crop_advantages_radar.xAxis,
                        axisLabel: { 
                            rotate: 45,
                            fontSize: 10
                        }
                    },
                    yAxis: { 
                        type: 'value', 
                        name: '温度(°C)',
                        nameTextStyle: { fontSize: 12 }
                    },
                    series: charts_data.crop_advantages_radar.series.map(s => ({
                        ...s,
                        itemStyle: {
                            color: s.name === '最低温度' ? '#4ECDC4' : '#FF6B6B'
                        }
                    }))
                });
                console.log('✅ 作物温度需求图设置完成');
            }
            
            // pH需求分布饼图
            if (charts_data.limiting_factors_pie && charts_data.limiting_factors_pie.data && charts.limitingFactorsChart) {
                console.log('🥧 设置pH需求饼图，数据点:', charts_data.limiting_factors_pie.data.length);
                charts.limitingFactorsChart.setOption({
                    title: { 
                        text: charts_data.limiting_factors_pie.title || '作物pH需求分布',
                        left: 'center',
                        textStyle: { fontSize: 16, fontWeight: 'bold' }
                    },
                    tooltip: { 
                        trigger: 'item',
                        formatter: '{a} <br/>{b}: {c}种作物 ({d}%)'
                    },
                    legend: { 
                        orient: 'vertical', 
                        left: 'left',
                        top: 'middle'
                    },
                    series: [{
                        name: 'pH需求',
                        type: 'pie',
                        radius: ['30%', '70%'],
                        center: ['60%', '50%'],
                        data: charts_data.limiting_factors_pie.data,
                        emphasis: { 
                            itemStyle: { 
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        },
                        label: {
                            show: true,
                            formatter: '{b}\n{c}种'
                        }
                    }]
                });
                console.log('✅ pH需求饼图设置完成');
            }
            
            console.log('✅ 作物图表加载完成');
        } else {
            console.error('作物分析API返回错误:', result.message);
        }
    } catch (error) {
        console.error('加载作物图表失败:', error);
    }
}

// 将作物图表功能添加到ChartLoader
if (window.ChartLoader) {
    window.ChartLoader.loadCropCharts = loadCropCharts;
} else {
    window.ChartLoader = { loadCropCharts };
}
