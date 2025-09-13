import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json
import base64
from io import BytesIO
from loguru import logger

class ChartService:
    """金融图表服务 - 生成各种金融分析图表"""
    
    def __init__(self):
        self.colors = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'success': '#2ca02c',
            'danger': '#d62728',
            'warning': '#ff7f0e',
            'info': '#17becf',
            'light': '#f8f9fa',
            'dark': '#343a40'
        }
    
    async def generate_price_chart(self, symbol: str, price_data: List[Dict[str, Any]], 
                                 chart_type: str = "candlestick") -> Dict[str, Any]:
        """生成价格图表（K线图、折线图等）"""
        try:
            df = pd.DataFrame(price_data)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            
            if chart_type == "candlestick":
                fig = go.Figure(data=[go.Candlestick(
                    x=df.index,
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'],
                    name='价格'
                )])
            else:
                fig = go.Figure(data=[go.Scatter(
                    x=df.index,
                    y=df['close'],
                    mode='lines',
                    name='收盘价',
                    line=dict(color=self.colors['primary'])
                )])
            
            # 设置图表布局
            fig.update_layout(
                title=f"{symbol} 价格走势",
                xaxis_title="日期",
                yaxis_title="价格",
                template="plotly_white",
                height=500,
                showlegend=True
            )
            
            return self._fig_to_dict(fig)
            
        except Exception as e:
            logger.error(f"生成价格图表失败: {str(e)}")
            return self._get_error_chart("价格图表生成失败")
    
    async def generate_technical_indicators(self, symbol: str, price_data: List[Dict[str, Any]], 
                                          indicators: List[str] = ["sma", "rsi", "macd"]) -> Dict[str, Any]:
        """生成技术指标图表"""
        try:
            df = pd.DataFrame(price_data)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            
            # 创建子图
            fig = go.Figure()
            
            # 价格图
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['close'],
                mode='lines',
                name='收盘价',
                line=dict(color=self.colors['primary']),
                yaxis='y'
            ))
            
            # 添加技术指标
            if "sma" in indicators:
                sma_20 = df['close'].rolling(window=20).mean()
                sma_50 = df['close'].rolling(window=50).mean()
                
                fig.add_trace(go.Scatter(
                    x=df.index,
                    y=sma_20,
                    mode='lines',
                    name='SMA 20',
                    line=dict(color=self.colors['success'], dash='dash'),
                    yaxis='y'
                ))
                
                fig.add_trace(go.Scatter(
                    x=df.index,
                    y=sma_50,
                    mode='lines',
                    name='SMA 50',
                    line=dict(color=self.colors['danger'], dash='dash'),
                    yaxis='y'
                ))
            
            if "rsi" in indicators and len(df) >= 14:
                # 计算RSI
                delta = df['close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))
                
                fig.add_trace(go.Scatter(
                    x=df.index,
                    y=rsi,
                    mode='lines',
                    name='RSI',
                    line=dict(color=self.colors['info']),
                    yaxis='y2'
                ))
            
            if "macd" in indicators and len(df) >= 26:
                # 计算MACD
                exp12 = df['close'].ewm(span=12, adjust=False).mean()
                exp26 = df['close'].ewm(span=26, adjust=False).mean()
                macd = exp12 - exp26
                signal = macd.ewm(span=9, adjust=False).mean()
                histogram = macd - signal
                
                fig.add_trace(go.Scatter(
                    x=df.index,
                    y=macd,
                    mode='lines',
                    name='MACD',
                    line=dict(color=self.colors['warning']),
                    yaxis='y3'
                ))
                
                fig.add_trace(go.Scatter(
                    x=df.index,
                    y=signal,
                    mode='lines',
                    name='Signal',
                    line=dict(color=self.colors['danger']),
                    yaxis='y3'
                ))
                
                fig.add_trace(go.Bar(
                    x=df.index,
                    y=histogram,
                    name='Histogram',
                    marker_color=self.colors['info'],
                    yaxis='y3'
                ))
            
            # 设置布局
            fig.update_layout(
                title=f"{symbol} 技术指标分析",
                xaxis=dict(title="日期", domain=[0, 0.95]),
                yaxis=dict(title="价格", domain=[0.7, 1]),
                yaxis2=dict(title="RSI", domain=[0.4, 0.65], range=[0, 100]),
                yaxis3=dict(title="MACD", domain=[0, 0.35]),
                template="plotly_white",
                height=600,
                showlegend=True
            )
            
            return self._fig_to_dict(fig)
            
        except Exception as e:
            logger.error(f"生成技术指标图表失败: {str(e)}")
            return self._get_error_chart("技术指标图表生成失败")
    
    async def generate_volume_chart(self, symbol: str, volume_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成成交量图表"""
        try:
            df = pd.DataFrame(volume_data)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            
            fig = go.Figure(data=[go.Bar(
                x=df.index,
                y=df['volume'],
                name='成交量',
                marker_color=self.colors['info']
            )])
            
            fig.update_layout(
                title=f"{symbol} 成交量分析",
                xaxis_title="日期",
                yaxis_title="成交量",
                template="plotly_white",
                height=400,
                showlegend=True
            )
            
            return self._fig_to_dict(fig)
            
        except Exception as e:
            logger.error(f"生成成交量图表失败: {str(e)}")
            return self._get_error_chart("成交量图表生成失败")
    
    async def generate_financial_ratio_chart(self, symbol: str, ratios: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """生成财务比率图表"""
        try:
            fig = go.Figure()
            
            for ratio_name, ratio_data in ratios.items():
                df = pd.DataFrame(ratio_data)
                df['period'] = pd.to_datetime(df['period'])
                
                fig.add_trace(go.Scatter(
                    x=df['period'],
                    y=df['value'],
                    mode='lines+markers',
                    name=ratio_name,
                    line=dict(width=2)
                ))
            
            fig.update_layout(
                title=f"{symbol} 财务比率趋势",
                xaxis_title="期间",
                yaxis_title="比率值",
                template="plotly_white",
                height=500,
                showlegend=True
            )
            
            return self._fig_to_dict(fig)
            
        except Exception as e:
            logger.error(f"生成财务比率图表失败: {str(e)}")
            return self._get_error_chart("财务比率图表生成失败")
    
    async def generate_sector_comparison(self, sector_data: List[Dict[str, Any]], 
                                        metric: str = "pe_ratio") -> Dict[str, Any]:
        """生成行业对比图表"""
        try:
            df = pd.DataFrame(sector_data)
            
            fig = go.Figure(data=[go.Bar(
                x=df['sector'],
                y=df[metric],
                name=metric.upper(),
                marker_color=px.colors.qualitative.Set3
            )])
            
            fig.update_layout(
                title=f"行业{metric.upper()}对比",
                xaxis_title="行业",
                yaxis_title=metric.upper(),
                template="plotly_white",
                height=500,
                showlegend=True
            )
            
            return self._fig_to_dict(fig)
            
        except Exception as e:
            logger.error(f"生成行业对比图表失败: {str(e)}")
            return self._get_error_chart("行业对比图表生成失败")
    
    async def generate_portfolio_pie_chart(self, portfolio_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成投资组合饼图"""
        try:
            df = pd.DataFrame(portfolio_data)
            
            fig = go.Figure(data=[go.Pie(
                labels=df['symbol'],
                values=df['weight'],
                hole=0.3,
                textinfo='label+percent',
                marker_colors=px.colors.qualitative.Pastel
            )])
            
            fig.update_layout(
                title="投资组合分配",
                template="plotly_white",
                height=400,
                showlegend=True
            )
            
            return self._fig_to_dict(fig)
            
        except Exception as e:
            logger.error(f"生成投资组合饼图失败: {str(e)}")
            return self._get_error_chart("投资组合图表生成失败")
    
    async def generate_correlation_matrix(self, symbols: List[str], correlation_data: List[List[float]]) -> Dict[str, Any]:
        """生成相关性矩阵热力图"""
        try:
            fig = go.Figure(data=go.Heatmap(
                z=correlation_data,
                x=symbols,
                y=symbols,
                colorscale='RdBu_r',
                zmid=0,
                colorbar=dict(title="相关性")
            ))
            
            fig.update_layout(
                title="股票相关性矩阵",
                template="plotly_white",
                height=500,
                width=600
            )
            
            return self._fig_to_dict(fig)
            
        except Exception as e:
            logger.error(f"生成相关性矩阵失败: {str(e)}")
            return self._get_error_chart("相关性矩阵生成失败")
    
    async def generate_performance_comparison(self, performance_data: List[Dict[str, Any]], 
                                            benchmarks: List[str] = []) -> Dict[str, Any]:
        """生成业绩对比图表"""
        try:
            df = pd.DataFrame(performance_data)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            
            fig = go.Figure()
            
            # 添加主要资产
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['return'],
                mode='lines',
                name='投资组合',
                line=dict(color=self.colors['primary'], width=3)
            ))
            
            # 添加基准
            for benchmark in benchmarks:
                if benchmark in df.columns:
                    fig.add_trace(go.Scatter(
                        x=df.index,
                        y=df[benchmark],
                        mode='lines',
                        name=benchmark,
                        line=dict(color=self.colors['secondary'], width=2, dash='dash')
                    ))
            
            fig.update_layout(
                title="业绩对比分析",
                xaxis_title="日期",
                yaxis_title="累计收益率 (%)",
                template="plotly_white",
                height=500,
                showlegend=True
            )
            
            return self._fig_to_dict(fig)
            
        except Exception as e:
            logger.error(f"生成业绩对比图表失败: {str(e)}")
            return self._get_error_chart("业绩对比图表生成失败")
    
    def _fig_to_dict(self, fig: go.Figure) -> Dict[str, Any]:
        """将Plotly图表转换为字典格式"""
        try:
            # 转换为JSON
            chart_json = fig.to_json()
            chart_data = json.loads(chart_json)
            
            # 生成图片base64
            img_buffer = BytesIO()
            fig.write_image(img_buffer, format='png', scale=2)
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
            
            return {
                "success": True,
                "chart_type": "plotly",
                "chart_data": chart_data,
                "image_base64": f"data:image/png;base64,{img_base64}",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"图表转换失败: {str(e)}")
            return self._get_error_chart("图表格式转换失败")
    
    def _get_error_chart(self, error_message: str) -> Dict[str, Any]:
        """生成错误图表"""
        return {
            "success": False,
            "error": error_message,
            "chart_type": "error",
            "timestamp": datetime.now().isoformat()
        }
    
    async def generate_comprehensive_report(self, symbol: str, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """生成综合分析报告图表集"""
        charts = {}
        
        try:
            # 价格图表
            if 'price_data' in analysis_data:
                charts['price_chart'] = await self.generate_price_chart(
                    symbol, analysis_data['price_data'], 'candlestick'
                )
            
            # 技术指标图表
            if 'price_data' in analysis_data:
                charts['technical_chart'] = await self.generate_technical_indicators(
                    symbol, analysis_data['price_data'], ['sma', 'rsi', 'macd']
                )
            
            # 成交量图表
            if 'volume_data' in analysis_data:
                charts['volume_chart'] = await self.generate_volume_chart(
                    symbol, analysis_data['volume_data']
                )
            
            # 财务比率图表
            if 'financial_ratios' in analysis_data:
                charts['ratio_chart'] = await self.generate_financial_ratio_chart(
                    symbol, analysis_data['financial_ratios']
                )
            
            return {
                "success": True,
                "symbol": symbol,
                "charts": charts,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"生成综合报告图表失败: {str(e)}")
            return {
                "success": False,
                "error": f"生成综合报告图表失败: {str(e)}",
                "symbol": symbol,
                "timestamp": datetime.now().isoformat()
            }

# 全局图表服务实例
chart_service = ChartService()