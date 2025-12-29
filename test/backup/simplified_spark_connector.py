# -*- coding: utf-8 -*-
"""
简化版Spark MySQL连接器
使用Pandas模拟Spark功能，避免JDBC驱动问题
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
import numpy as np
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimplifiedSparkConnector:
    def __init__(self, mysql_config=None):
        """初始化简化版Spark连接器"""
        self.mysql_config = mysql_config or {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'wujiayun1',
            'database': 'climate_data'
        }
        
        self.connection = None
        self.data_cache = {}
        
        logger.info("✅ 简化版Spark连接器初始化成功")
    
    def connect_mysql(self):
        """连接MySQL数据库"""
        try:
            self.connection = mysql.connector.connect(**self.mysql_config)
            logger.info("✅ MySQL数据库连接成功")
            return True
        except Error as e:
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
            
            # 读取各个表（使用实际的表名）
            climate_df = self.read_mysql_table("temperature_data")
            precip_df = self.read_mysql_table("climate_precipitation") 
            soil_df = self.read_mysql_table("soil_profiles")
            crop_df = self.read_mysql_table("crop_requirements")
            
            # 合并气候数据
            if climate_df is not None and precip_df is not None:
                # 简单合并，假设按位置匹配
                climate_combined = pd.concat([climate_df, precip_df], ignore_index=True)
            else:
                climate_combined = climate_df if climate_df is not None else precip_df
            
            logger.info("✅ 所有农业数据读取完成")
            
            return {
                'climate': climate_combined,
                'soil': soil_df,
                'crop': crop_df,
                'suitability': None  # 暂时没有适宜性数据
            }
            
        except Exception as e:
            logger.error(f"❌ 读取农业数据失败: {e}")
            return None
    
    def analyze_climate_trends(self):
        """分析气候趋势"""
        try:
            logger.info("📊 开始分析气候趋势...")
            
            climate_df = self.data_cache.get('climate_data')
            if climate_df is None or climate_df.empty:
                return None
            
            # 年度温度趋势
            temp_trend = climate_df.groupby('year').agg({
                'temperature': ['mean', 'min', 'max'],
                'id': 'count'
            }).round(2)
            temp_trend.columns = ['avg_temp', 'min_temp', 'max_temp', 'record_count']
            temp_trend = temp_trend.reset_index()
            
            # 月度降水模式
            precip_pattern = climate_df.groupby('month').agg({
                'precipitation': ['mean', 'std'],
                'id': 'count'
            }).round(2)
            precip_pattern.columns = ['avg_precip', 'precip_std', 'record_count']
            precip_pattern = precip_pattern.reset_index()
            
            # 地区气候差异
            climate_df['lat_zone'] = climate_df['lat'].round(1)
            climate_df['lon_zone'] = climate_df['lon'].round(1)
            
            regional_climate = climate_df.groupby(['lat_zone', 'lon_zone']).agg({
                'avg_temperature': 'mean',
                'annual_precipitation': 'mean',
                'id': 'count'
            }).round(2)
            regional_climate.columns = ['avg_temp', 'avg_precip', 'record_count']
            regional_climate = regional_climate.reset_index()
            regional_climate = regional_climate[regional_climate['record_count'] >= 5]
            
            logger.info("✅ 气候趋势分析完成")
            
            return {
                'temperature_trend': temp_trend,
                'precipitation_pattern': precip_pattern,
                'regional_climate': regional_climate
            }
            
        except Exception as e:
            logger.error(f"❌ 气候趋势分析失败: {e}")
            return None
    
    def analyze_soil_distribution(self):
        """分析土壤分布"""
        try:
            logger.info("🌱 开始分析土壤分布...")
            
            soil_df = self.data_cache.get('soil_data')
            if soil_df is None or soil_df.empty:
                return None
            
            # 土壤类型分布
            soil_type_dist = soil_df.groupby(['soil_type', 'county']).agg({
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
            soil_df['ph_category'] = pd.cut(soil_df['ph_value'], 
                                          bins=[0, 5.5, 6.5, 7.5, 8.5, 14],
                                          labels=['强酸性(<5.5)', '酸性(5.5-6.5)', '中性(6.5-7.5)', '碱性(7.5-8.5)', '强碱性(>8.5)'])
            
            ph_distribution = soil_df.groupby('ph_category').agg({
                'id': 'count',
                'organic_matter': 'mean'
            }).round(2)
            ph_distribution.columns = ['count', 'avg_organic_matter']
            ph_distribution = ph_distribution.reset_index()
            
            # 县市土壤质量排名
            county_soil_quality = soil_df.groupby('county').agg({
                'id': 'count',
                'ph_value': 'mean',
                'organic_matter': 'mean',
                'total_nitrogen': 'mean',
                'available_phosphorus': 'mean',
                'available_potassium': 'mean'
            }).round(3)
            
            # 计算土壤质量评分
            county_soil_quality['soil_quality_score'] = (
                county_soil_quality['organic_matter'] * 0.3 +
                county_soil_quality['total_nitrogen'] * 1000 * 0.3 +
                county_soil_quality['available_phosphorus'] * 0.2 +
                county_soil_quality['available_potassium'] * 0.2
            ).round(2)
            
            county_soil_quality.columns = ['sample_count', 'avg_ph', 'avg_organic_matter', 'avg_nitrogen', 'avg_phosphorus', 'avg_potassium', 'soil_quality_score']
            county_soil_quality = county_soil_quality.reset_index()
            county_soil_quality = county_soil_quality[county_soil_quality['sample_count'] >= 10]
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
    
    def analyze_crop_suitability(self):
        """分析作物适宜性"""
        try:
            logger.info("🌾 开始分析作物适宜性...")
            
            suitability_df = self.data_cache.get('suitability_results')
            if suitability_df is None or suitability_df.empty:
                return None
            
            # 作物适宜性统计
            crop_suitability_stats = suitability_df.groupby(['crop_name', 'suitability_level']).agg({
                'id': 'count',
                'comprehensive_suitability': 'mean',
                'temp_suitability': 'mean',
                'precip_suitability': 'mean',
                'soil_suitability': 'mean'
            }).round(4)
            crop_suitability_stats.columns = ['area_count', 'avg_suitability', 'avg_temp_suitability', 'avg_precip_suitability', 'avg_soil_suitability']
            crop_suitability_stats = crop_suitability_stats.reset_index()
            
            # 最佳种植区域推荐
            suitable_areas = suitability_df[suitability_df['suitability_level'].isin(['高度适宜', '中度适宜'])]
            best_planting_areas = suitable_areas.groupby(['crop_name', 'county']).agg({
                'id': 'count',
                'comprehensive_suitability': 'mean',
                'lat': 'mean',
                'lon': 'mean'
            }).round(4)
            best_planting_areas.columns = ['suitable_points', 'avg_suitability', 'center_lat', 'center_lon']
            best_planting_areas = best_planting_areas.reset_index()
            best_planting_areas = best_planting_areas[best_planting_areas['suitable_points'] >= 5]
            best_planting_areas = best_planting_areas.sort_values(['crop_name', 'avg_suitability'], ascending=[True, False])
            
            # 区划优化建议
            zoning_optimization = suitability_df.groupby(['zone_id', 'crop_name']).agg({
                'id': 'count',
                'comprehensive_suitability': 'mean',
                'center_lat': 'mean',
                'center_lon': 'mean',
                'county': lambda x: list(set(x))
            }).round(4)
            zoning_optimization.columns = ['grid_count', 'avg_suitability', 'zone_center_lat', 'zone_center_lon', 'counties']
            zoning_optimization = zoning_optimization.reset_index()
            zoning_optimization = zoning_optimization[zoning_optimization['grid_count'] >= 10]
            zoning_optimization = zoning_optimization.sort_values(['zone_id', 'avg_suitability'], ascending=[True, False])
            
            # 限制因子分析
            unsuitable_areas = suitability_df[suitability_df['suitability_level'].isin(['勉强适宜', '不适宜'])]
            
            def get_limiting_factor(row):
                factors = {
                    'temp_suitability': '温度限制',
                    'precip_suitability': '降水限制',
                    'soil_suitability': '土壤限制'
                }
                min_factor = min(row['temp_suitability'], row['precip_suitability'], row['soil_suitability'])
                for factor, name in factors.items():
                    if row[factor] == min_factor:
                        return name
                return '土壤限制'
            
            unsuitable_areas['limiting_factor'] = unsuitable_areas.apply(get_limiting_factor, axis=1)
            
            limiting_factors = unsuitable_areas.groupby(['crop_name', 'limiting_factor']).agg({
                'id': 'count',
                'comprehensive_suitability': 'mean'
            }).round(4)
            limiting_factors.columns = ['affected_areas', 'avg_suitability']
            limiting_factors = limiting_factors.reset_index()
            
            logger.info("✅ 作物适宜性分析完成")
            
            return {
                'crop_suitability_stats': crop_suitability_stats,
                'best_planting_areas': best_planting_areas,
                'zoning_optimization': zoning_optimization,
                'limiting_factors': limiting_factors
            }
            
        except Exception as e:
            logger.error(f"❌ 作物适宜性分析失败: {e}")
            return None
    
    def generate_comprehensive_report(self):
        """生成综合分析报告"""
        try:
            logger.info("📋 开始生成综合分析报告...")
            
            # 获取所有分析结果
            climate_analysis = self.analyze_climate_trends()
            soil_analysis = self.analyze_soil_distribution()
            crop_analysis = self.analyze_crop_suitability()
            
            # 组织报告数据
            report_data = {}
            
            if climate_analysis:
                report_data['climate'] = climate_analysis
            
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
    print("🌱 简化版Spark农业分析系统测试")
    print("=" * 50)
    
    # 创建连接器
    connector = SimplifiedSparkConnector()
    
    try:
        # 读取数据
        data = connector.read_all_agricultural_data()
        if not data:
            print("❌ 数据读取失败")
            return
        
        # 生成分析报告
        report = connector.generate_comprehensive_report()
        if report:
            print("🎉 分析报告生成成功！")
            
            # 显示部分结果
            if 'climate' in report:
                print("\n📊 气候趋势分析:")
                print(report['climate']['temperature_trend'].head())
            
            if 'soil' in report:
                print("\n🌱 土壤质量排名:")
                print(report['soil']['county_soil_quality'].head())
            
            if 'crop' in report:
                print("\n🌾 作物适宜性统计:")
                print(report['crop']['crop_suitability_stats'].head())
        
    except Exception as e:
        print(f"❌ 系统运行失败: {e}")
    
    finally:
        connector.close()


if __name__ == '__main__':
    main()
