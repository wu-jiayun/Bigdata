# -*- coding: utf-8 -*-
"""
真实数据连接器
适配实际MySQL数据库表结构
"""

import pandas as pd
import pymysql
import numpy as np
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RealDataConnector:
    def __init__(self, mysql_config=None):
        """初始化真实数据连接器"""
        self.mysql_config = mysql_config or {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'wujiayun1',
            'database': 'climate_data',
            'charset': 'utf8mb4'
        }
        
        self.connection = None
        self.data_cache = {}
        
        logger.info("✅ 真实数据连接器初始化成功")
    
    def connect_mysql(self):
        """连接MySQL数据库"""
        try:
            self.connection = pymysql.connect(**self.mysql_config)
            logger.info("✅ MySQL数据库连接成功")
            return True
        except Exception as e:
            logger.error(f"❌ MySQL连接失败: {e}")
            return False
    
    def read_mysql_table(self, table_name, conditions=None):
        """从MySQL读取表数据"""
        try:
            if not self.connection:
                if not self.connect_mysql():
                    return None
            
            # 构建查询
            query = f"SELECT * FROM {table_name}"
            if conditions:
                query += f" WHERE {conditions}"
            
            # 读取数据
            df = pd.read_sql(query, self.connection)
            logger.info(f"✅ 成功读取表 {table_name}: {len(df)} 条记录")
            
            # 缓存数据
            self.data_cache[table_name] = df
            
            return df
            
        except Exception as e:
            logger.error(f"❌ 读取MySQL表失败: {e}")
            return None
    
    def read_all_agricultural_data(self):
        """读取所有农业数据"""
        try:
            logger.info("🚀 开始读取所有农业数据...")
            
            # 读取各个表
            temp_df = self.read_mysql_table("temperature_data")
            precip_df = self.read_mysql_table("climate_precipitation") 
            soil_df = self.read_mysql_table("soil_profiles")
            crop_df = self.read_mysql_table("crop_requirements")
            
            logger.info("✅ 所有农业数据读取完成")
            
            return {
                'temperature': temp_df,
                'precipitation': precip_df,
                'soil': soil_df,
                'crop': crop_df
            }
            
        except Exception as e:
            logger.error(f"❌ 读取农业数据失败: {e}")
            return None
    
    def analyze_temperature_trends(self):
        """分析温度趋势"""
        try:
            logger.info("🌡️ 开始分析温度趋势...")
            
            temp_df = self.data_cache.get('temperature_data')
            if temp_df is None or temp_df.empty:
                return None
            
            # 年度温度趋势
            temp_trend = temp_df[['year_val', 'winter', 'spring', 'summer', 'autumn', 'annual']].copy()
            temp_trend = temp_trend.dropna()
            
            # 月度温度模式 - 计算各月平均值
            monthly_cols = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 
                           'jul', 'aug', 'sep', 'oct_val', 'nov', 'dec_val']
            monthly_data = []
            
            for i, col in enumerate(monthly_cols, 1):
                if col in temp_df.columns:
                    avg_temp = temp_df[col].mean()
                    if not pd.isna(avg_temp):
                        monthly_data.append({
                            'month': i,
                            'month_name': f'{i}月',
                            'avg_temp': round(avg_temp, 2)
                        })
            
            monthly_pattern = pd.DataFrame(monthly_data)
            
            logger.info("✅ 温度趋势分析完成")
            
            return {
                'annual_trend': temp_trend,
                'monthly_pattern': monthly_pattern
            }
            
        except Exception as e:
            logger.error(f"❌ 温度趋势分析失败: {e}")
            return None
    
    def analyze_soil_distribution(self):
        """分析土壤分布"""
        try:
            logger.info("🌱 开始分析土壤分布...")
            
            soil_df = self.data_cache.get('soil_profiles')
            if soil_df is None or soil_df.empty:
                return None
            
            # 土壤类型分布
            soil_type_dist = soil_df.groupby(['soil_name', 'county_name']).agg({
                'id': 'count',
                'ph_value': 'mean',
                'organic_matter': 'mean',
                'total_nitrogen': 'mean',
                'available_phosphorus': 'mean',
                'available_potassium': 'mean'
            }).round(3)
            soil_type_dist.columns = ['count', 'avg_ph', 'avg_organic_matter', 'avg_nitrogen', 'avg_phosphorus', 'avg_potassium']
            soil_type_dist = soil_type_dist.reset_index()
            
            # pH值分布统计
            soil_df_clean = soil_df.dropna(subset=['ph_value'])
            soil_df_clean['ph_category'] = pd.cut(soil_df_clean['ph_value'], 
                                          bins=[0, 5.5, 6.5, 7.5, 8.5, 14],
                                          labels=['强酸性(<5.5)', '酸性(5.5-6.5)', '中性(6.5-7.5)', '碱性(7.5-8.5)', '强碱性(>8.5)'])
            
            ph_distribution = soil_df_clean.groupby('ph_category').agg({
                'id': 'count',
                'organic_matter': 'mean'
            }).round(2)
            ph_distribution.columns = ['count', 'avg_organic_matter']
            ph_distribution = ph_distribution.reset_index()
            
            # 县市土壤质量排名
            county_soil_quality = soil_df.groupby('county_name').agg({
                'id': 'count',
                'ph_value': 'mean',
                'organic_matter': 'mean',
                'total_nitrogen': 'mean',
                'available_phosphorus': 'mean',
                'available_potassium': 'mean'
            }).round(3)
            
            # 计算土壤质量评分
            county_soil_quality['soil_quality_score'] = (
                county_soil_quality['organic_matter'].fillna(0) * 0.3 +
                county_soil_quality['total_nitrogen'].fillna(0) * 100 * 0.3 +
                county_soil_quality['available_phosphorus'].fillna(0) * 0.2 +
                county_soil_quality['available_potassium'].fillna(0) * 0.2
            ).round(2)
            
            county_soil_quality.columns = ['sample_count', 'avg_ph', 'avg_organic_matter', 'avg_nitrogen', 'avg_phosphorus', 'avg_potassium', 'soil_quality_score']
            county_soil_quality = county_soil_quality.reset_index()
            county_soil_quality = county_soil_quality[county_soil_quality['sample_count'] >= 5]
            county_soil_quality = county_soil_quality.sort_values('soil_quality_score', ascending=False)
            
            logger.info("✅ 土壤分布分析完成")
            
            return {
                'soil_type_distribution': soil_type_dist,
                'ph_distribution': ph_distribution,
                'county_soil_quality': county_soil_quality
            }
            
        except Exception as e:
            logger.error(f"❌ 土壤分布分析失败: {e}")
            return None
    
    def analyze_crop_requirements(self):
        """分析作物需求"""
        try:
            logger.info("🌾 开始分析作物需求...")
            
            crop_df = self.data_cache.get('crop_requirements')
            if crop_df is None or crop_df.empty:
                return None
            
            # 作物温度需求分析
            temp_requirements = crop_df[['category', 'crop_type', 'min_temperature_min', 'min_temperature_max', 
                                       'optimal_temperature_min', 'optimal_temperature_max', 
                                       'max_temperature_min', 'max_temperature_max']].copy()
            temp_requirements = temp_requirements.dropna()
            
            # 作物pH需求分析
            ph_requirements = crop_df[['category', 'crop_type', 'ph_min', 'ph_max']].copy()
            ph_requirements = ph_requirements.dropna()
            
            # 作物分类统计
            crop_categories = crop_df.groupby('category').agg({
                'id': 'count',
                'crop_type': 'nunique'
            })
            crop_categories.columns = ['total_varieties', 'unique_types']
            crop_categories = crop_categories.reset_index()
            
            logger.info("✅ 作物需求分析完成")
            
            return {
                'temperature_requirements': temp_requirements,
                'ph_requirements': ph_requirements,
                'crop_categories': crop_categories
            }
            
        except Exception as e:
            logger.error(f"❌ 作物需求分析失败: {e}")
            return None
    
    def generate_comprehensive_report(self):
        """生成综合分析报告"""
        try:
            logger.info("📋 开始生成综合分析报告...")
            
            # 获取所有分析结果
            temp_analysis = self.analyze_temperature_trends()
            soil_analysis = self.analyze_soil_distribution()
            crop_analysis = self.analyze_crop_requirements()
            
            # 组织报告数据
            report_data = {}
            
            if temp_analysis:
                report_data['temperature'] = temp_analysis
            
            if soil_analysis:
                report_data['soil'] = soil_analysis
            
            if crop_analysis:
                report_data['crop'] = crop_analysis
            
            logger.info("✅ 综合分析报告生成完成")
            return report_data
            
        except Exception as e:
            logger.error(f"❌ 生成综合报告失败: {e}")
            return None
    
    def close(self):
        """关闭连接"""
        if self.connection:
            self.connection.close()
            logger.info("🔒 MySQL连接已关闭")


def main():
    """测试主函数"""
    print("🌱 真实数据农业分析系统测试")
    print("=" * 50)
    
    # 创建连接器
    connector = RealDataConnector()
    
    try:
        # 读取数据
        data = connector.read_all_agricultural_data()
        if not data:
            print("❌ 数据读取失败")
            return
        
        print("📊 数据读取成功:")
        for key, df in data.items():
            if df is not None:
                print(f"  - {key}: {len(df)} 条记录")
        
        # 生成分析报告
        report = connector.generate_comprehensive_report()
        if report:
            print("\n🎉 分析报告生成成功！")
            
            # 显示部分结果
            if 'temperature' in report:
                print("\n🌡️ 温度趋势分析:")
                if 'monthly_pattern' in report['temperature']:
                    print(report['temperature']['monthly_pattern'])
            
            if 'soil' in report:
                print("\n🌱 土壤质量排名:")
                if 'county_soil_quality' in report['soil']:
                    print(report['soil']['county_soil_quality'].head())
            
            if 'crop' in report:
                print("\n🌾 作物分类统计:")
                if 'crop_categories' in report['crop']:
                    print(report['crop']['crop_categories'])
        
    except Exception as e:
        print(f"❌ 系统运行失败: {e}")
    
    finally:
        connector.close()


if __name__ == '__main__':
    main()
