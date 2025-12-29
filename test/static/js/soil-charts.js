/**
 * 沃土规划师 - 土壤图表模块
 * 包含土壤分析相关的图表加载功能
 */

/**
 * 加载土壤图表
 */
async function loadSoilCharts() {
    try {
        console.log('🌱 开始加载土壤图表...');
        
        // 检查SparkCore是否存在
        if (!window.SparkCore || !window.SparkCore.charts) {
            console.error('❌ SparkCore.charts 未初始化');
            return;
        }
        
        const charts = window.SparkCore.charts;
        console.log('🔍 检查土壤图表容器:', {
            soilTypePieChart: !!charts.soilTypePieChart,
            phDistChart: !!charts.phDistChart,
            countyQualityChart: !!charts.countyQualityChart
        });
        
        // 确保图表容器已初始化
        if (!charts.soilTypePieChart || !charts.phDistChart || !charts.countyQualityChart) {
            console.error('❌ 土壤图表容器未初始化');
            return;
        }
        
        const response = await fetch('/api/echarts/soil_analysis');
        const result = await response.json();
        
        console.log('📊 土壤分析API响应:', result);
        
        if (result.status === 'success') {
            const charts_data = result.charts;
            console.log('📈 土壤图表数据:', Object.keys(charts_data));
            
            // 土壤类型饼图
            if (charts_data.soil_type_pie && charts_data.soil_type_pie.data && charts_data.soil_type_pie.data.length > 0) {
                console.log('🥧 设置土壤类型饼图，数据点:', charts_data.soil_type_pie.data.length);
                console.log('📊 土壤类型数据:', charts_data.soil_type_pie.data);
                
                const pieOption = {
                    title: { 
                        text: '湖南省土壤类型分布',
                        left: 'center',
                        textStyle: { fontSize: 16, fontWeight: 'bold' }
                    },
                    tooltip: { 
                        trigger: 'item',
                        formatter: '{a} <br/>{b}: {c}个样本 ({d}%)'
                    },
                    legend: { 
                        orient: 'vertical', 
                        left: 'left',
                        top: 'middle',
                        textStyle: { fontSize: 12 }
                    },
                    series: [{
                        name: '土壤类型',
                        type: 'pie',
                        radius: ['30%', '70%'],
                        center: ['60%', '50%'],
                        data: charts_data.soil_type_pie.data,
                        emphasis: { 
                            itemStyle: { 
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        },
                        label: {
                            show: true,
                            formatter: '{b}\n{c}个'
                        },
                        labelLine: {
                            show: true
                        }
                    }]
                };
                
                window.SparkCore.charts.soilTypePieChart.setOption(pieOption);
                console.log('✅ 土壤类型饼图设置完成');
            } else {
                console.warn('⚠️ 土壤类型数据为空或格式错误');
            }
            
            // pH分布图
            if (charts_data.ph_distribution && charts_data.ph_distribution.xAxis && charts_data.ph_distribution.xAxis.length > 0) {
                console.log('📊 设置pH分布图，X轴数据:', charts_data.ph_distribution.xAxis.length);
                console.log('📈 pH分布数据:', charts_data.ph_distribution);
                
                const phOption = {
                    title: { 
                        text: '湖南省土壤pH值分布',
                        left: 'center',
                        textStyle: { fontSize: 16, fontWeight: 'bold' }
                    },
                    tooltip: { 
                        trigger: 'axis',
                        axisPointer: { type: 'shadow' },
                        formatter: '{a}<br/>{b}: {c}个样本'
                    },
                    xAxis: { 
                        type: 'category',
                        data: charts_data.ph_distribution.xAxis,
                        axisLabel: { 
                            rotate: 0,
                            fontSize: 12
                        }
                    },
                    yAxis: { 
                        type: 'value', 
                        name: '样本数量',
                        nameLocation: 'middle',
                        nameGap: 50,
                        nameTextStyle: { fontSize: 12 }
                    },
                    series: charts_data.ph_distribution.series.map(s => ({
                        ...s,
                        itemStyle: {
                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                {offset: 0, color: '#4ECDC4'},
                                {offset: 1, color: '#44A08D'}
                            ])
                        },
                        emphasis: {
                            itemStyle: {
                                color: '#2E8B57'
                            }
                        }
                    }))
                };
                
                window.SparkCore.charts.phDistChart.setOption(phOption);
                console.log('✅ pH分布图设置完成');
            } else {
                console.warn('⚠️ pH分布数据为空或格式错误');
            }
            
            // 县市质量排名图
            if (charts_data.county_quality_ranking && charts_data.county_quality_ranking.xAxis && charts_data.county_quality_ranking.xAxis.length > 0) {
                console.log('🏆 设置县市质量排名，县市数量:', charts_data.county_quality_ranking.xAxis.length);
                console.log('📊 县市排名数据:', charts_data.county_quality_ranking);
                
                const qualityOption = {
                    title: { 
                        text: '湖南省县市土壤质量排名',
                        left: 'center',
                        textStyle: { fontSize: 16, fontWeight: 'bold' }
                    },
                    tooltip: { 
                        trigger: 'axis',
                        axisPointer: { type: 'shadow' },
                        formatter: '{a}<br/>{b}: {c}分'
                    },
                    xAxis: { 
                        type: 'category',
                        data: charts_data.county_quality_ranking.xAxis,
                        axisLabel: { 
                            rotate: 45,
                            interval: 0,
                            fontSize: 11
                        }
                    },
                    yAxis: { 
                        type: 'value', 
                        name: '土壤质量评分',
                        nameLocation: 'middle',
                        nameGap: 50,
                        nameTextStyle: { fontSize: 12 }
                    },
                    series: charts_data.county_quality_ranking.series.map(s => ({
                        ...s,
                        itemStyle: {
                            color: function(params) {
                                // 根据排名设置不同颜色
                                const colors = ['#FFD700', '#C0C0C0', '#CD7F32', '#4ECDC4', '#45B7D1'];
                                return colors[params.dataIndex % colors.length];
                            }
                        },
                        emphasis: {
                            itemStyle: {
                                color: '#FF6B6B'
                            }
                        },
                        label: {
                            show: true,
                            position: 'top',
                            formatter: '{c}',
                            fontSize: 10
                        }
                    }))
                };
                
                window.SparkCore.charts.countyQualityChart.setOption(qualityOption);
                console.log('✅ 县市质量排名图设置完成');
            } else {
                console.warn('⚠️ 县市质量排名数据为空或格式错误');
            }
            
            console.log('✅ 土壤图表加载完成');
        } else {
            console.error('土壤分析API返回错误:', result.message);
        }
    } catch (error) {
        console.error('加载土壤图表失败:', error);
    }
}

// 将土壤图表功能添加到ChartLoader
if (window.ChartLoader) {
    window.ChartLoader.loadSoilCharts = loadSoilCharts;
} else {
    window.ChartLoader = { loadSoilCharts };
}
