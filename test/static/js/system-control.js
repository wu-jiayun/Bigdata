/**
 * 沃土规划师 - 系统控制模块
 * 包含系统初始化、分析运行等控制功能
 */

/**
 * 初始化Spark系统
 */
async function initializeSystem() {
    const btn = document.getElementById('initSystemBtn');
    const info = document.getElementById('systemInfo');
    
    if (!btn || !info) {
        console.error('❌ 初始化按钮或信息元素不存在');
        return;
    }
    
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>初始化中...';
    info.className = 'alert alert-info';
    info.innerHTML = '<i class="fas fa-cog fa-spin me-2"></i>正在初始化Spark系统，连接MySQL数据库...';
    
    try {
        console.log('🚀 开始初始化系统...');
        const response = await fetch('/api/system/initialize', {
            method: 'POST'
        });
        const result = await response.json();
        console.log('📊 初始化结果:', result);
        
        if (result.status === 'success') {
            window.SparkCore.systemInitialized = true;
            info.className = 'alert alert-success';
            
            const summary = result.data_summary;
            info.innerHTML = `<i class="fas fa-check-circle me-2"></i>Spark系统初始化成功！数据摘要: 温度${summary.temperature_records || 0}条, 降水${summary.precipitation_records || 0}条, 土壤${summary.soil_records || 0}条, 作物${summary.crop_types || 0}种`;
            
            const runBtn = document.getElementById('runAnalysisBtn');
            if (runBtn) runBtn.disabled = false;
        } else {
            throw new Error(result.message);
        }
    } catch (error) {
        console.error('❌ 初始化失败:', error);
        info.className = 'alert alert-danger';
        info.innerHTML = `<i class="fas fa-exclamation-triangle me-2"></i>初始化失败: ${error.message}`;
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-rocket me-2"></i>重新初始化';
    }
}

/**
 * 运行综合分析
 */
async function runAnalysis() {
    const btn = document.getElementById('runAnalysisBtn');
    const info = document.getElementById('analysisInfo');
    
    // 检查元素是否存在
    if (!btn) {
        console.error('❌ runAnalysisBtn 元素不存在');
        return;
    }
    if (!info) {
        console.error('❌ analysisInfo 元素不存在');
        return;
    }
    
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>分析中...';
    info.className = 'alert alert-info';
    info.innerHTML = '<i class="fas fa-cog fa-spin me-2"></i>正在运行Spark综合分析，请稍候...';
    
    // 设置30秒超时
    const timeoutId = setTimeout(() => {
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-chart-line me-2"></i>重新分析';
        }
        if (info) {
            info.className = 'alert alert-warning';
            info.innerHTML = '<i class="fas fa-clock me-2"></i>分析超时，请重试或刷新页面';
        }
    }, 30000);
    
    try {
        console.log('🚀 开始运行分析...');
        const response = await fetch('/api/analysis/run', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        clearTimeout(timeoutId); // 清除超时
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const result = await response.json();
        console.log('📊 分析结果:', result);
        
        if (result.status === 'success') {
            window.SparkCore.analysisCompleted = true;
            info.className = 'alert alert-success';
            info.innerHTML = `<i class="fas fa-check-circle me-2"></i>分析完成！执行时间: ${result.statistics.execution_time}秒`;
            
            console.log('📈 开始加载所有图表...');
            
            // 立即更新按钮状态
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-chart-line me-2"></i>重新分析';
            
            // 加载图表
            try {
                await window.ChartLoader.loadAllCharts();
                info.innerHTML += '<br><i class="fas fa-chart-bar me-2"></i>图表加载完成！';
            } catch (chartError) {
                console.error('图表加载失败:', chartError);
                info.innerHTML += '<br><i class="fas fa-exclamation-triangle me-2"></i>图表加载失败，请刷新页面重试';
            }
        } else {
            throw new Error(result.message);
        }
    } catch (error) {
        console.error('❌ 分析失败:', error);
        clearTimeout(timeoutId); // 确保清除超时
        info.className = 'alert alert-danger';
        info.innerHTML = `<i class="fas fa-exclamation-triangle me-2"></i>分析失败: ${error.message}`;
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-chart-line me-2"></i>重新分析';
    }
}

/**
 * 检查分析状态
 */
async function checkAnalysisStatus() {
    try {
        const response = await fetch('/api/echarts/soil_analysis');
        const result = await response.json();
        
        if (result.status === 'success') {
            console.log('✅ 检测到分析已完成，开始加载图表...');
            window.SparkCore.analysisCompleted = true;
            
            const info = document.getElementById('analysisInfo');
            const btn = document.getElementById('runAnalysisBtn');
            
            if (info) {
                info.className = 'alert alert-success';
                info.innerHTML = '<i class="fas fa-check-circle me-2"></i>分析完成！正在加载图表...';
            }
            
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-chart-line me-2"></i>重新分析';
            }
            
            await window.ChartLoader.loadAllCharts();
            
            if (info) {
                info.innerHTML += '<br><i class="fas fa-chart-bar me-2"></i>图表加载完成！';
            }
            
            return true;
        }
    } catch (error) {
        console.log('检查分析状态失败:', error);
    }
    return false;
}

// 导出系统控制功能
window.SystemControl = {
    initializeSystem,
    runAnalysis,
    checkAnalysisStatus
};
