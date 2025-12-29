# -*- coding: utf-8 -*-
"""
Spark MySQL连接器
基于Spark的MySQL数据读取和处理模块
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import mysql.connector
from mysql.connector import Error
import pandas as pd
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SparkMySQLConnector:
    def __init__(self, mysql_config=None):
        """初始化Spark MySQL连接器"""
        self.mysql_config = mysql_config or {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'wujiayun1',
            'database': 'agricultural_db'
        }
        
        # 初始化Spark会话
        self.spark = SparkSession.builder \
            .appName("沃土规划师农业分析系统") \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
            .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
            .getOrCreate()
        
        # 设置日志级别
        self.spark.sparkContext.setLogLevel("WARN")
        
        logger.info("✅ Spark会话初始化成功")
    
    def read_mysql_table(self, table_name, conditions=None):
        """从MySQL读取表数据到Spark DataFrame"""
        try:
            # 构建JDBC URL
            jdbc_url = f"jdbc:mysql://{self.mysql_config['host']}:{self.mysql_config['port']}/{self.mysql_config['database']}"
            
            # JDBC连接属性
            properties = {
                "user": self.mysql_config['user'],
                "password": self.mysql_config['password'],
                "driver": "com.mysql.cj.jdbc.Driver",
                "characterEncoding": "utf8",
                "useUnicode": "true"
            }
            
            # 构建查询
            if conditions:
                query = f"(SELECT * FROM {table_name} WHERE {conditions}) AS subquery"
            else:
                query = table_name
            
            # 读取数据
            df = self.spark.read \
                .format("jdbc") \
                .option("url", jdbc_url) \
                .option("dbtable", query) \
                .option("user", properties["user"]) \
                .option("password", properties["password"]) \
                .option("driver", properties["driver"]) \
                .load()
            
            logger.info(f"✅ 成功读取表 {table_name}: {df.count()} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 读取MySQL表失败: {e}")
            return None
    
    def read_all_agricultural_data(self):
        """读取所有农业数据"""
        try:
            logger.info("🚀 开始读取所有农业数据...")
            
            # 读取各个表
            climate_df = self.read_mysql_table("climate_data")
            soil_df = self.read_mysql_table("soil_data")
            crop_df = self.read_mysql_table("crop_requirements")
            suitability_df = self.read_mysql_table("suitability_results")
            
            # 创建临时视图用于SQL查询
            if climate_df:
                climate_df.createOrReplaceTempView("climate_data")
            if soil_df:
                soil_df.createOrReplaceTempView("soil_data")
            if crop_df:
                crop_df.createOrReplaceTempView("crop_requirements")
            if suitability_df:
                suitability_df.createOrReplaceTempView("suitability_results")
            
            logger.info("✅ 所有农业数据读取完成并创建临时视图")
            
            return {
                'climate': climate_df,
                'soil': soil_df,
                'crop': crop_df,
                'suitability': suitability_df
            }
            
        except Exception as e:
            logger.error(f"❌ 读取农业数据失败: {e}")
            return None
    
    def analyze_climate_trends(self):
        """分析气候趋势"""
        try:
            logger.info("📊 开始分析气候趋势...")
            
            # 年度温度趋势
            temp_trend = self.spark.sql("""
                SELECT 
                    year,
                    ROUND(AVG(temperature), 2) as avg_temp,
                    ROUND(MIN(temperature), 2) as min_temp,
                    ROUND(MAX(temperature), 2) as max_temp,
                    COUNT(*) as record_count
                FROM climate_data 
                WHERE year IS NOT NULL AND temperature IS NOT NULL
                GROUP BY year 
                ORDER BY year
            """)
            
            # 月度降水模式
            precip_pattern = self.spark.sql("""
                SELECT 
                    month,
                    ROUND(AVG(precipitation), 2) as avg_precip,
                    ROUND(STDDEV(precipitation), 2) as precip_std,
                    COUNT(*) as record_count
                FROM climate_data 
                WHERE month IS NOT NULL AND precipitation IS NOT NULL
                GROUP BY month 
                ORDER BY month
            """)
            
            # 地区气候差异
            regional_climate = self.spark.sql("""
                SELECT 
                    ROUND(lat, 1) as lat_zone,
                    ROUND(lon, 1) as lon_zone,
                    ROUND(AVG(avg_temperature), 2) as avg_temp,
                    ROUND(AVG(annual_precipitation), 2) as avg_precip,
                    COUNT(*) as record_count
                FROM climate_data 
                WHERE lat IS NOT NULL AND lon IS NOT NULL
                GROUP BY ROUND(lat, 1), ROUND(lon, 1)
                HAVING COUNT(*) >= 5
                ORDER BY lat_zone, lon_zone
            """)
            
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
            
            # 土壤类型分布
            soil_type_dist = self.spark.sql("""
                SELECT 
                    soil_type,
                    county,
                    COUNT(*) as count,
                    ROUND(AVG(ph_value), 2) as avg_ph,
                    ROUND(AVG(organic_matter), 2) as avg_organic_matter,
                    ROUND(AVG(total_nitrogen), 3) as avg_nitrogen,
                    ROUND(AVG(available_phosphorus), 2) as avg_phosphorus,
                    ROUND(AVG(available_potassium), 2) as avg_potassium
                FROM soil_data 
                WHERE soil_type IS NOT NULL
                GROUP BY soil_type, county
                ORDER BY soil_type, count DESC
            """)
            
            # pH值分布统计
            ph_distribution = self.spark.sql("""
                SELECT 
                    CASE 
                        WHEN ph_value < 5.5 THEN '强酸性(<5.5)'
                        WHEN ph_value < 6.5 THEN '酸性(5.5-6.5)'
                        WHEN ph_value < 7.5 THEN '中性(6.5-7.5)'
                        WHEN ph_value < 8.5 THEN '碱性(7.5-8.5)'
                        ELSE '强碱性(>8.5)'
                    END as ph_category,
                    COUNT(*) as count,
                    ROUND(AVG(organic_matter), 2) as avg_organic_matter
                FROM soil_data 
                WHERE ph_value IS NOT NULL
                GROUP BY 
                    CASE 
                        WHEN ph_value < 5.5 THEN '强酸性(<5.5)'
                        WHEN ph_value < 6.5 THEN '酸性(5.5-6.5)'
                        WHEN ph_value < 7.5 THEN '中性(6.5-7.5)'
                        WHEN ph_value < 8.5 THEN '碱性(7.5-8.5)'
                        ELSE '强碱性(>8.5)'
                    END
                ORDER BY count DESC
            """)
            
            # 县市土壤质量排名
            county_soil_quality = self.spark.sql("""
                SELECT 
                    county,
                    COUNT(*) as sample_count,
                    ROUND(AVG(ph_value), 2) as avg_ph,
                    ROUND(AVG(organic_matter), 2) as avg_organic_matter,
                    ROUND(AVG(total_nitrogen), 3) as avg_nitrogen,
                    ROUND(AVG(available_phosphorus), 2) as avg_phosphorus,
                    ROUND(AVG(available_potassium), 2) as avg_potassium,
                    ROUND(
                        (AVG(organic_matter) * 0.3 + 
                         AVG(total_nitrogen) * 1000 * 0.3 + 
                         AVG(available_phosphorus) * 0.2 + 
                         AVG(available_potassium) * 0.2), 2
                    ) as soil_quality_score
                FROM soil_data 
                WHERE county IS NOT NULL
                GROUP BY county
                HAVING COUNT(*) >= 10
                ORDER BY soil_quality_score DESC
            """)
            
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
            
            # 作物适宜性统计
            crop_suitability_stats = self.spark.sql("""
                SELECT 
                    crop_name,
                    suitability_level,
                    COUNT(*) as area_count,
                    ROUND(AVG(comprehensive_suitability), 4) as avg_suitability,
                    ROUND(AVG(temp_suitability), 4) as avg_temp_suitability,
                    ROUND(AVG(precip_suitability), 4) as avg_precip_suitability,
                    ROUND(AVG(soil_suitability), 4) as avg_soil_suitability
                FROM suitability_results 
                GROUP BY crop_name, suitability_level
                ORDER BY crop_name, avg_suitability DESC
            """)
            
            # 最佳种植区域推荐
            best_planting_areas = self.spark.sql("""
                SELECT 
                    crop_name,
                    county,
                    COUNT(*) as suitable_points,
                    ROUND(AVG(comprehensive_suitability), 4) as avg_suitability,
                    ROUND(AVG(lat), 4) as center_lat,
                    ROUND(AVG(lon), 4) as center_lon
                FROM suitability_results 
                WHERE suitability_level IN ('高度适宜', '中度适宜')
                GROUP BY crop_name, county
                HAVING COUNT(*) >= 5
                ORDER BY crop_name, avg_suitability DESC
            """)
            
            # 区划优化建议
            zoning_optimization = self.spark.sql("""
                SELECT 
                    zone_id,
                    crop_name,
                    COUNT(*) as grid_count,
                    ROUND(AVG(comprehensive_suitability), 4) as avg_suitability,
                    ROUND(AVG(center_lat), 4) as zone_center_lat,
                    ROUND(AVG(center_lon), 4) as zone_center_lon,
                    COLLECT_SET(county) as counties
                FROM suitability_results 
                WHERE zone_id IS NOT NULL
                GROUP BY zone_id, crop_name
                HAVING COUNT(*) >= 10
                ORDER BY zone_id, avg_suitability DESC
            """)
            
            # 限制因子分析
            limiting_factors = self.spark.sql("""
                SELECT 
                    crop_name,
                    CASE 
                        WHEN temp_suitability = LEAST(temp_suitability, precip_suitability, soil_suitability) 
                        THEN '温度限制'
                        WHEN precip_suitability = LEAST(temp_suitability, precip_suitability, soil_suitability) 
                        THEN '降水限制'
                        ELSE '土壤限制'
                    END as limiting_factor,
                    COUNT(*) as affected_areas,
                    ROUND(AVG(comprehensive_suitability), 4) as avg_suitability
                FROM suitability_results 
                WHERE suitability_level IN ('勉强适宜', '不适宜')
                GROUP BY crop_name, 
                    CASE 
                        WHEN temp_suitability = LEAST(temp_suitability, precip_suitability, soil_suitability) 
                        THEN '温度限制'
                        WHEN precip_suitability = LEAST(temp_suitability, precip_suitability, soil_suitability) 
                        THEN '降水限制'
                        ELSE '土壤限制'
                    END
                ORDER BY crop_name, affected_areas DESC
            """)
            
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
            
            # 转换为Pandas DataFrame用于导出
            report_data = {}
            
            if climate_analysis:
                report_data['climate'] = {
                    'temperature_trend': climate_analysis['temperature_trend'].toPandas(),
                    'precipitation_pattern': climate_analysis['precipitation_pattern'].toPandas(),
                    'regional_climate': climate_analysis['regional_climate'].toPandas()
                }
            
            if soil_analysis:
                report_data['soil'] = {
                    'soil_type_distribution': soil_analysis['soil_type_distribution'].toPandas(),
                    'ph_distribution': soil_analysis['ph_distribution'].toPandas(),
                    'county_soil_quality': soil_analysis['county_soil_quality'].toPandas()
                }
            
            if crop_analysis:
                report_data['crop'] = {
                    'crop_suitability_stats': crop_analysis['crop_suitability_stats'].toPandas(),
                    'best_planting_areas': crop_analysis['best_planting_areas'].toPandas(),
                    'zoning_optimization': crop_analysis['zoning_optimization'].toPandas(),
                    'limiting_factors': crop_analysis['limiting_factors'].toPandas()
                }
            
            logger.info("✅ 综合分析报告生成完成")
            return report_data
            
        except Exception as e:
            logger.error(f"❌ 生成综合报告失败: {e}")
            return None
    
    def close(self):
        """关闭Spark会话"""
        if self.spark:
            self.spark.stop()
            logger.info("🔒 Spark会话已关闭")


def main():
    """测试主函数"""
    print("🌱 沃土规划师 - Spark MySQL数据分析系统")
    print("=" * 60)
    
    # 创建连接器
    connector = SparkMySQLConnector()
    
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
