import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, Typography, Progress, List, Avatar, Spin, Alert, Space } from 'tdesign-react';
import { LineChartIcon, UserIcon, TrendUpIcon, DollarIcon, BookIcon } from 'tdesign-icons-react';

const { Title, Text, Paragraph } = Typography;

interface MarketData {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
}

interface RecentActivity {
  id: string;
  type: string;
  title: string;
  time: string;
  user: string;
}

// 模拟数据
const mockMarketData: MarketData[] = [
  { symbol: 'AAPL', name: '苹果公司', price: 178.72, change: 2.15, changePercent: 1.22 },
  { symbol: 'MSFT', name: '微软公司', price: 415.50, change: 3.25, changePercent: 0.79 },
  { symbol: 'GOOGL', name: '谷歌', price: 155.20, change: -1.30, changePercent: -0.83 },
  { symbol: 'TSLA', name: '特斯拉', price: 245.60, change: 8.75, changePercent: 3.69 },
  { symbol: 'AMZN', name: '亚马逊', price: 185.25, change: 1.45, changePercent: 0.79 }
];

const mockActivities: RecentActivity[] = [
  { id: '1', type: 'analysis', title: '完成了苹果公司技术面分析', time: '2分钟前', user: '分析师张' },
  { id: '2', type: 'report', title: '生成了微软财务分析报告', time: '5分钟前', user: '研究员李' },
  { id: '3', type: 'search', title: '搜索了新能源行业数据', time: '10分钟前', user: '投资经理王' },
  { id: '4', type: 'chart', title: '创建了特斯拉股价走势图', time: '15分钟前', user: '数据分析师赵' },
  { id: '5', type: 'knowledge', title: '上传了最新监管政策文件', time: '30分钟前', user: '知识库管理员' }
];

const Dashboard: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(true);
  const [marketData, setMarketData] = useState<MarketData[]>([]);
  const [recentActivities, setRecentActivities] = useState<RecentActivity[]>([]);
  const [error, setError] = useState<string>('');

  const fetchDashboardData = async () => {
    setLoading(true);
    setError('');

    try {
      // 模拟API调用延迟
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // 使用模拟数据
      setMarketData(mockMarketData);
      setRecentActivities(mockActivities);

    } catch (err) {
      setError(err instanceof Error ? err.message : '获取数据失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const renderMarketChange = (change: number, changePercent: number) => {
    const isPositive = change >= 0;
    const color = isPositive ? '#52c41a' : '#f5222d';
    const sign = isPositive ? '+' : '';

    return (
      <span style={{ color, fontWeight: 500 }}>
        {sign}{change.toFixed(2)} ({sign}{changePercent.toFixed(2)}%)
      </span>
    );
  };

  if (loading) {
    return (
      <div style={{ padding: '40px', textAlign: 'center' }}>
        <Spin size="large" />
        <Text style={{ display: 'block', marginTop: '16px' }}>正在加载仪表盘数据...</Text>
      </div>
    );
  }

  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>智能投研仪表盘</Title>
      
      {error && (
        <Alert theme="error" style={{ marginBottom: '16px' }}>
          {error}
        </Alert>
      )}

      {/* 概览统计 */}
      <Row gutter={16} style={{ marginBottom: '24px' }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="总分析次数"
              value={1258}
              prefix={<TrendUpIcon />}
              valueStyle={{ color: '#1890ff' }}
            />
            <Progress percentage={75} style={{ marginTop: '8px' }} />
            <Text type="secondary" style={{ fontSize: '12px' }}>本月同比增长 15%</Text>
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="知识库文档"
              value={892}
              prefix={<BookIcon />}
              valueStyle={{ color: '#52c41a' }}
            />
            <Progress percentage={60} style={{ marginTop: '8px' }} />
            <Text type="secondary" style={{ fontSize: '12px' }}>新增 45 篇文档</Text>
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="用户活跃度"
              value={89}
              suffix="%"
              valueStyle={{ color: '#faad14' }}
            />
            <Progress percentage={89} style={{ marginTop: '8px' }} />
            <Text type="secondary" style={{ fontSize: '12px' }}>较上周提升 5%</Text>
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="投资回报率"
              value={18.7}
              suffix="%"
              prefix={<DollarIcon />}
              valueStyle={{ color: '#f5222d' }}
            />
            <Progress percentage={87} style={{ marginTop: '8px' }} />
            <Text type="secondary" style={{ fontSize: '12px' }}>年化收益率</Text>
          </Card>
        </Col>
      </Row>

      {/* 市场行情 */}
      <Row gutter={16} style={{ marginBottom: '24px' }}>
        <Col span={12}>
          <Card title="热门股票行情" extra={<a>查看更多</a>}>
            {marketData.length > 0 ? (
              <List
                split
                data={marketData}
                render={(item) => (
                  <List.Item>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
                      <div>
                        <Text strong>{item.name}</Text>
                        <br />
                        <Text type="secondary">{item.symbol}</Text>
                      </div>
                      <div style={{ textAlign: 'right' }}>
                        <Text strong>${item.price.toFixed(2)}</Text>
                        <br />
                        {renderMarketChange(item.change, item.changePercent)}
                      </div>
                    </div>
                  </List.Item>
                )}
              />
            ) : (
              <div style={{ textAlign: 'center', padding: '20px', color: '#999' }}>
                <LineChartIcon style={{ fontSize: '32px', marginBottom: '8px' }} />
                <Text>暂无市场数据</Text>
              </div>
            )}
          </Card>
        </Col>

        <Col span={12}>
          <Card title="最近活动" extra={<a>查看全部</a>}>
            {recentActivities.length > 0 ? (
              <List
                split
                data={recentActivities.slice(0, 5)}
                render={(item) => (
                  <List.Item>
                    <div style={{ display: 'flex', alignItems: 'center' }}>
                      <Avatar style={{ marginRight: '12px', backgroundColor: '#1890ff' }}>
                        {item.user.charAt(0)}
                      </Avatar>
                      <div>
                        <Text>{item.title}</Text>
                        <br />
                        <Text type="secondary" size="small">
                          {item.user} • {item.time}
                        </Text>
                      </div>
                    </div>
                  </List.Item>
                )}
              />
            ) : (
              <div style={{ textAlign: 'center', padding: '20px', color: '#999' }}>
                <UserIcon style={{ fontSize: '32px', marginBottom: '8px' }} />
                <Text>暂无活动记录</Text>
              </div>
            )}
          </Card>
        </Col>
      </Row>

      {/* 快速访问 */}
      <Row gutter={16}>
        <Col span={8}>
          <Card 
            hover 
            style={{ textAlign: 'center', cursor: 'pointer' }}
            onClick={() => window.location.href = '/analysis'}
          >
            <LineChartIcon style={{ fontSize: '48px', color: '#1890ff', marginBottom: '12px' }} />
            <Title level={4}>股票分析</Title>
            <Text type="secondary">深度技术面和基本面分析</Text>
          </Card>
        </Col>
        <Col span={8}>
          <Card 
            hover 
            style={{ textAlign: 'center', cursor: 'pointer' }}
            onClick={() => window.location.href = '/knowledge'}
          >
            <BookIcon style={{ fontSize: '48px', color: '#52c41a', marginBottom: '12px' }} />
            <Title level={4}>知识库</Title>
            <Text type="secondary">海量金融研究报告</Text>
          </Card>
        </Col>
        <Col span={8}>
          <Card 
            hover 
            style={{ textAlign: 'center', cursor: 'pointer' }}
            onClick={() => window.location.href = '/chat'}
          >
            <UserIcon style={{ fontSize: '48px', color: '#faad14', marginBottom: '12px' }} />
            <Title level={4}>智能助手</Title>
            <Text type="secondary">AI投研问答</Text>
          </Card>
        </Col>
      </Row>

      {/* 系统状态 */}
      <Card title="系统状态" style={{ marginTop: '24px' }}>
        <Row gutter={16}>
          <Col span={6}>
            <div style={{ textAlign: 'center' }}>
              <Progress
                type="circle"
                percentage={100}
                color="#52c41a"
                label="API服务"
              />
              <Text strong style={{ display: 'block', marginTop: '8px' }}>正常运行</Text>
            </div>
          </Col>
          <Col span={6}>
            <div style={{ textAlign: 'center' }}>
              <Progress
                type="circle"
                percentage={95}
                color="#1890ff"
                label="数据更新"
              />
              <Text strong style={{ display: 'block', marginTop: '8px' }}>实时同步</Text>
            </div>
          </Col>
          <Col span={6}>
            <div style={{ textAlign: 'center' }}>
              <Progress
                type="circle"
                percentage={100}
                color="#faad14"
                label="AI模型"
              />
              <Text strong style={{ display: 'block', marginTop: '8px' }}>多模型可用</Text>
            </div>
          </Col>
          <Col span={6}>
            <div style={{ textAlign: 'center' }}>
              <Progress
                type="circle"
                percentage={99.9}
                color="#f5222d"
                label="系统可用性"
              />
              <Text strong style={{ display: 'block', marginTop: '8px' }}>高可用</Text>
            </div>
          </Col>
        </Row>
      </Card>
    </div>
  );
};

export default Dashboard;