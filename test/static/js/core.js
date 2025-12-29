/**
 * 沃土规划师 - 核心功能模块
 * 包含全局变量、图表初始化、系统状态管理等核心功能
 */

// 全局变量
let charts = {};
let systemInitialized = false;
let analysisCompleted = false;

/**
 * 初始化图表容器
 */
function initCharts() {
    const chartIds = [
        'tempTrendChart', 'precipPatternChart', 'climateHeatmapChart',
        'soilTypePieChart', 'phDistChart', 'countyQualityChart',
        'suitabilityDistChart', 'cropRadarChart', 'limitingFactorsChart',
        'zoningScatterChart', 'optimizationMapChart'
    ];

    console.log('🔄 开始初始化图表容器...');
    
    chartIds.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            // 检查容器尺寸
            const rect = element.getBoundingClientRect();
            console.log(`📊 容器 ${id}: ${rect.width}x${rect.height}`);
            
            if (rect.width > 0 && rect.height > 0) {
                try {
                    charts[id] = echarts.init(element);
                    console.log(`✅ ${id} 初始化成功`);
                } catch (error) {
                    console.error(`❌ ${id} 初始化失败:`, error);
                }
            } else {
                console.warn(`⚠️ ${id} 容器尺寸为0，延迟初始化`);
                // 延迟初始化
                setTimeout(() => {
                    const newRect = element.getBoundingClientRect();
                    if (newRect.width > 0 && newRect.height > 0) {
                        charts[id] = echarts.init(element);
                        console.log(`✅ ${id} 延迟初始化成功`);
                    }
                }, 1000);
            }
        } else {
            console.error(`❌ 找不到容器: ${id}`);
        }
    });
    
    console.log(`📊 图表容器初始化完成，成功: ${Object.keys(charts).length}/${chartIds.length}`);
}

/**
 * 更新系统状态
 * @param {string} status - 状态类型: ready, loading, error
 * @param {string} message - 状态消息
 */
function updateSystemStatus(status, message) {
    const statusIndicator = document.getElementById('systemStatus');
    const statusText = document.getElementById('statusText');
    
    if (!statusIndicator || !statusText) return;
    
    statusIndicator.className = 'status-indicator';
    
    switch(status) {
        case 'ready':
            statusIndicator.classList.add('status-ready');
            break;
        case 'loading':
            statusIndicator.classList.add('status-loading');
            break;
        case 'error':
            statusIndicator.classList.add('status-error');
            break;
    }
    
    statusText.textContent = `系统状态: ${message}`;
}

/**
 * 检查系统状态
 */
async function checkSystemStatus() {
    try {
        const response = await fetch('/api/system/status');
        const result = await response.json();
        
        if (result.spark_initialized) {
            systemInitialized = true;
            updateSystemStatus('ready', '系统就绪');
            const runBtn = document.getElementById('runAnalysisBtn');
            if (runBtn) runBtn.disabled = false;
        }
    } catch (error) {
        console.error('检查系统状态失败:', error);
    }
}

/**
 * 窗口大小改变时重新调整图表
 */
function handleWindowResize() {
    Object.values(charts).forEach(chart => {
        if (chart) chart.resize();
    });
}

// 导出核心功能
window.SparkCore = {
    charts,
    systemInitialized,
    analysisCompleted,
    initCharts,
    updateSystemStatus,
    checkSystemStatus,
    handleWindowResize
};
