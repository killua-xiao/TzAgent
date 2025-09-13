import React, { useState, useEffect } from 'react';
import { Card, Button, Input, Select, Space, Typography, Spin, Alert } from 'tdesign-react';
import { LineChart, BarChart, PieChart, Grid, SearchIcon } from 'tdesign-icons-react';
import { echarts } from 'echarts';

const { Title, Text } = Typography;
const { Option } = Select;

interface StockData {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
  volume: number;
  marketCap: number;
}

interface ChartData {
  type: string;
  data: any[];
  options: any;
}

const AnalysisPage: React.FC = () => {
  const [symbol, setSymbol] = useState<string>('');
  const [period, setPeriod] = useState<string>('1m');
  const [chartType, setChartType] = useState<string>('line');
  const [loading, setLoading] = useState<boolean>(false);
  const [stockData, setStockData] = useState<StockData | null>(null);
  const [chartData, setChartData] = useState<ChartData | null>(null);
  const [error, setError] = useState<string>('');

  const periods = [
    { value: '1d', label: '1日' },
    { value: '1w', label: '1周' },
    { value: '1m', label: '1月' },
    { value: '3m', label: '3月' },
    { value: '6m', label: '6月' },
    { value: '1y', label: '1年' },
    { value: '2y', label: '2年' },
    { value: '5y', label: '5年' }
  ];

  const chartTypes = [
    { value: 'line', label: '折线图', icon: <LineChart /> },
    { value: 'candlestick', label: 'K线图', icon: <BarChart /> },
    { value: 'volume', label: '成交量', icon: <BarChart /> },
    { value: 'technical', label: '技术指标', icon: <Grid /> }
  ];

  const fetchStockData = async () => {
    if (!symbol.trim()) {
      setError('请输入股票代码');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // 获取股票基本信息
      const stockResponse = await fetch(`/api/v1/market/quote/${symbol}`);
      if (!stockResponse.ok) {
        throw new Error('获取股票数据失败');
      }
      const stock = await stockResponse.json();
      setStockData(stock);

      // 获取图表数据
      const chartResponse = await fetch(`/api/v1/charts/price/${symbol}?period=${period}&chart_type=${chartType}`);
      if (!chartResponse.ok) {
        throw new Error('获取图表数据失败');
      }
      const chart = await chartResponse.json();
      setChartData(chart);

    } catch (err) {
      setError(err instanceof Error ? err.message : '获取数据失败');
    } finally {
      setLoading(false);
    }
  };

  const renderPriceChange = (change: number, changePercent: number) => {
    const isPositive = change >= 0;
    const color = isPositive ? 'green' : 'red';
    const sign = isPositive ? '+' : '';

    return (
      <Space size="small">
        <Text style={{ color, fontSize: '18px', fontWeight: 'bold' }}>
          {sign}{change.toFixed(2)}
        </Text>
        <Text style={{ color, fontSize: '14px' }}>
          ({sign}{changePercent.toFixed(2)}%)
        </Text>
      </Space>
    );
  };

  const renderChart = () => {
    if (!chartData) return null;

    switch (chartData.type) {
      case 'line':
        return (
          <div style={{ height: '400px' }}>
            {/* ECharts 折线图渲染 */}
          </div>
        );
      case 'candlestick':
        return (
          <div style={{ height: '400px' }}>
            {/* ECharts K线图渲染 */}
          </div>
        );
      case 'volume':
        return (
          <div style={{ height: '300px' }}>
            {/* ECharts 成交量图渲染 */}
          </div>
        );
      default:
        return null;
    }
  };

  useEffect(() => {
    if (symbol) {
      fetchStockData();
    }
  }, [period, chartType]);

  return (
    <div style={{ padding: '24px', maxWidth: '1200px', margin: '0 auto' }}>
      <Title level={2}>股票分析</Title>
      
      {/* 搜索和控制区域 */}
      <Card>
        <Space size="large" align="center">
          <Input
            placeholder="输入股票代码，如：AAPL, 000001.SZ"
            value={symbol}
            onChange={setSymbol}
            style={{ width: '200px' }}
            prefix={<SearchIcon />}
          />
          
          <Select
            value={period}
            onChange={setPeriod}
            style={{ width: '120px' }}
          >
            {periods.map(p => (
              <Option key={p.value} value={p.value} label={p.label} />
            ))}
          </Select>

          <Select
            value={chartType}
            onChange={setChartType}
            style={{ width: '120px' }}
          >
            {chartTypes.map(t => (
              <Option key={t.value} value={t.value} label={t.label} />
            ))}
          </Select>

          <Button
            theme="primary"
            onClick={fetchStockData}
            loading={loading}
            disabled={!symbol.trim()}
          >
            分析
          </Button>
        </Space>
      </Card>

      {error && (
        <Alert theme="error" style={{ marginTop: '16px' }}>
          {error}
        </Alert>
      )}

      {loading && (
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <Spin size="large" />
          <Text style={{ display: 'block', marginTop: '16px' }}>正在分析数据...</Text>
        </div>
      )}

      {stockData && !loading && (
        <>
          {/* 股票基本信息 */}
          <Card style={{ marginTop: '16px' }}>
            <Space size="large" align="center">
              <div>
                <Title level={3}>{stockData.name}</Title>
                <Text type="secondary">{stockData.symbol}</Text>
              </div>
              
              <div>
                <Title level={2} style={{ margin: 0 }}>
                  ${stockData.price.toFixed(2)}
                </Title>
                {renderPriceChange(stockData.change, stockData.changePercent)}
              </div>

              <div>
                <Text>成交量: {(stockData.volume / 1000000).toFixed(2)}M</Text>
                <br />
                <Text>市值: ${(stockData.marketCap / 1000000000).toFixed(2)}B</Text>
              </div>
            </Space>
          </Card>

          {/* 图表区域 */}
          <Card style={{ marginTop: '16px' }}>
            <Title level={4}>价格走势</Title>
            {renderChart()}
          </Card>

          {/* 技术指标区域 */}
          <Card style={{ marginTop: '16px' }}>
            <Title level={4}>技术指标</Title>
            <Space size="large">
              <Button variant="outline">MACD</Button>
              <Button variant="outline">RSI</Button>
              <Button variant="outline">布林带</Button>
              <Button variant="outline">移动平均线</Button>
            </Space>
          </Card>

          {/* 基本面分析 */}
          <Card style={{ marginTop: '16px' }}>
            <Title level={4}>基本面分析</Title>
            <Space size="large">
              <Button variant="outline">财务比率</Button>
              <Button variant="outline">盈利能力</Button>
              <Button variant="outline">估值指标</Button>
              <Button variant="outline">成长性</Button>
            </Space>
          </Card>
        </>
      )}
    </div>
  );
};

export default AnalysisPage;