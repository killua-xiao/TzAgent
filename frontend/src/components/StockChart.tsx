import React from 'react';
import { Card, Spin, Message } from 'tdesign-react';
import ReactECharts from 'echarts-for-react';
import { useQuery } from 'react-query';
import { stockApi } from '../services/api';
import type { StockData } from '../types';

interface StockChartProps {
  symbol: string;
  period?: string;
  height?: number;
}

const StockChart: React.FC<StockChartProps> = ({ 
  symbol, 
  period = '1y', 
  height = 300 
}) => {
  const { data, isLoading, error } = useQuery(
    ['stockChart', symbol, period],
    () => stockApi.batchGetStocks([symbol]),
    {
      enabled: !!symbol,
      staleTime: 5 * 60 * 1000,
    }
  );

  if (error) {
    Message.error(`图表数据加载失败: ${error.message}`);
    return (
      <Card title={`${symbol} 价格走势`} className="h-full">
        <div className="text-center py-12 text-gray-400">
          <div className="text-lg">数据加载失败</div>
          <div className="text-sm mt-1">请检查股票代码是否正确</div>
        </div>
      </Card>
    );
  }

  if (isLoading) {
    return (
      <Card title={`${symbol} 价格走势`} className="h-full">
        <Spin size="large" className="py-12" />
      </Card>
    );
  }

  const stockData = data?.data?.[0];
  if (!stockData) {
    return (
      <Card title={`${symbol} 价格走势`} className="h-full">
        <div className="text-center py-12 text-gray-400">
          <div className="text-lg">暂无数据</div>
        </div>
      </Card>
    );
  }

  // 模拟历史价格数据
  const generateHistoricalData = () => {
    const basePrice = stockData.price;
    const data = [];
    const now = new Date();
    
    for (let i = 30; i >= 0; i--) {
      const date = new Date(now);
      date.setDate(date.getDate() - i);
      
      const volatility = Math.random() * 0.03 - 0.015; // -1.5% 到 +1.5%
      const price = basePrice * (1 + volatility);
      
      data.push({
        date: date.toISOString().split('T')[0],
        price: Number(price.toFixed(2)),
        volume: Math.floor(Math.random() * 1000000) + 500000
      });
    }
    
    return data;
  };

  const chartData = generateHistoricalData();

  const option = {
    title: {
      text: `${stockData.name} (${stockData.symbol})`,
      subtext: `当前价格: ¥${stockData.price.toFixed(2)} | 涨跌幅: ${stockData.changePercent >= 0 ? '+' : ''}${stockData.changePercent.toFixed(2)}%`,
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      },
      formatter: function (params: any) {
        const data = params[0];
        return `
          <div style="font-weight: bold; margin-bottom: 5px;">${data.name}</div>
          <div>价格: ¥${data.value.toFixed(2)}</div>
          <div>市值: ¥${(stockData.marketCap / 1e8).toFixed(2)}亿</div>
        `;
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: chartData.map(item => item.date),
      axisLine: {
        lineStyle: {
          color: '#ddd'
        }
      }
    },
    yAxis: {
      type: 'value',
      axisLine: {
        show: false
      },
      axisLabel: {
        formatter: '¥{value}'
      },
      splitLine: {
        lineStyle: {
          type: 'dashed',
          color: '#eee'
        }
      }
    },
    series: [
      {
        name: '价格',
        type: 'line',
        data: chartData.map(item => item.price),
        smooth: true,
        symbol: 'circle',
        symbolSize: 6,
        itemStyle: {
          color: stockData.changePercent >= 0 ? '#00b96b' : '#f56c6c'
        },
        lineStyle: {
          color: stockData.changePercent >= 0 ? '#00b96b' : '#f56c6c',
          width: 2
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [{
              offset: 0,
              color: stockData.changePercent >= 0 ? 'rgba(0, 185, 107, 0.3)' : 'rgba(245, 108, 108, 0.3)'
            }, {
              offset: 1,
              color: stockData.changePercent >= 0 ? 'rgba(0, 185, 107, 0.1)' : 'rgba(245, 108, 108, 0.1)'
            }]
          }
        }
      }
    ],
    dataZoom: [
      {
        type: 'inside',
        start: 0,
        end: 100
      }
    ]
  };

  return (
    <Card title={`${stockData.name} (${stockData.symbol}) 价格走势`} className="h-full">
      <ReactECharts
        option={option}
        style={{ height: height, width: '100%' }}
        opts={{ renderer: 'canvas' }}
      />
      <div className="mt-4 text-sm text-gray-500 grid grid-cols-2 gap-4">
        <div>
          <div className="font-medium">当前价格</div>
          <div className={`text-lg font-bold ${stockData.changePercent >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            ¥{stockData.price.toFixed(2)}
          </div>
        </div>
        <div>
          <div className="font-medium">涨跌幅</div>
          <div className={`text-lg font-bold ${stockData.changePercent >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {stockData.changePercent >= 0 ? '+' : ''}{stockData.changePercent.toFixed(2)}%
          </div>
        </div>
        <div>
          <div className="font-medium">市值</div>
          <div className="text-lg font-bold text-gray-800">
            ¥{(stockData.marketCap / 1e8).toFixed(2)}亿
          </div>
        </div>
        <div>
          <div className="font-medium">行业</div>
          <div className="text-lg font-bold text-gray-800">
            {stockData.industry}
          </div>
        </div>
      </div>
    </Card>
  );
};

export default StockChart;