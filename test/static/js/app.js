/**
 * 沃土规划师 - 主应用初始化文件
 * 负责页面加载完成后的初始化工作
 */

// 确保所有模块加载完成后再初始化
function waitForModules(callback) {
    const checkModules = () => {
        if (typeof echarts !== 'undefined' && 
            window.SparkCore && 
            window.SystemControl && 
            window.ChartLoader) {
            callback();
        } else {
            console.log('⏳ 等待模块加载...');
            setTimeout(checkModules, 100);
        }
    };
    checkModules();
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 页面加载完成，开始初始化...');
    
    waitForModules(() => {
        console.log('✅ 所有模块已加载完成');
        
        // 检查ECharts是否加载
        if (typeof echarts === 'undefined') {
            console.error('❌ ECharts库未加载！');
            alert('ECharts库加载失败，请刷新页面重试');
            return;
        } else {
            console.log('✅ ECharts库已加载，版本:', echarts.version);
        }
        
        // 初始化图表
        try {
            window.SparkCore.initCharts();
            console.log('✅ 图表容器初始化完成');
            
            // 验证图表容器
            const chartCount = Object.keys(window.SparkCore.charts).length;
            console.log(`📊 已初始化 ${chartCount} 个图表容器`);
            
            // 测试一个简单图表
            if (window.SparkCore.charts.tempTrendChart) {
                window.SparkCore.charts.tempTrendChart.setOption({
                    title: { text: '等待数据...' },
                    xAxis: { data: [] },
                    yAxis: {},
                    series: []
                });
                console.log('✅ 测试图表设置成功');
            }
            
        } catch (error) {
            console.error('❌ 图表初始化失败:', error);
        }
        
        initializeEventHandlers();
    });
});

// 初始化事件处理器
function initializeEventHandlers() {
    console.log('🔗 开始绑定事件处理器...');
    
    // 等待DOM完全加载后再绑定事件
    const bindEvents = () => {
        const initBtn = document.getElementById('initSystemBtn');
        const runBtn = document.getElementById('runAnalysisBtn');
        
        console.log('🔍 查找按钮元素:', {
            initBtn: !!initBtn,
            runBtn: !!runBtn
        });
        
        if (initBtn) {
            console.log('✅ 绑定初始化按钮事件');
            initBtn.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('🚀 初始化按钮被点击');
                window.SystemControl.initializeSystem();
            });
        } else {
            console.error('❌ 找不到初始化按钮 #initSystemBtn');
        }
        
        if (runBtn) {
            console.log('✅ 绑定分析按钮事件');
            runBtn.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('🔬 分析按钮被点击');
                window.SystemControl.runAnalysis();
            });
        } else {
            console.error('❌ 找不到分析按钮 #runAnalysisBtn');
        }
        
        // 检查系统状态
        if (window.SparkCore && window.SparkCore.checkSystemStatus) {
            window.SparkCore.checkSystemStatus();
        }
        
        // 检查是否有未完成的分析
        setTimeout(async () => {
            if (window.SystemControl && window.SystemControl.checkAnalysisStatus) {
                const analysisCompleted = await window.SystemControl.checkAnalysisStatus();
                if (analysisCompleted) {
                    console.log('🎉 检测到之前的分析已完成，图表已加载');
                }
            }
        }, 2000);
        
        console.log('🎉 事件绑定完成');
    };
    
    // 确保DOM已加载
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bindEvents);
    } else {
        bindEvents();
    }
}

// 窗口大小改变时重新调整图表
window.addEventListener('resize', function() {
    window.SparkCore.handleWindowResize();
});
