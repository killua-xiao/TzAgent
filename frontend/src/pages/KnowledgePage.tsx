import React, { useState, useEffect } from 'react';
import { Card, Button, Input, Table, Space, Typography, Tag, Spin, Alert } from 'tdesign-react';
import { SearchIcon, BookIcon, DownloadIcon } from 'tdesign-icons-react';

const { Title, Text } = Typography;

interface KnowledgeItem {
  id: string;
  title: string;
  category: string;
  source: string;
  publishDate: string;
  relevance: number;
  summary: string;
}

const KnowledgePage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [knowledgeData, setKnowledgeData] = useState<KnowledgeItem[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [error, setError] = useState<string>('');

  const categories = [
    { value: 'all', label: '全部' },
    { value: 'financial_reports', label: '财务报告' },
    { value: 'market_analysis', label: '市场分析' },
    { value: 'company_research', label: '公司研究' },
    { value: 'economic_data', label: '经济数据' },
    { value: 'investment_strategy', label: '投资策略' },
    { value: 'regulatory_documents', label: '监管文件' }
  ];

  const columns = [
    {
      title: '标题',
      colKey: 'title',
      width: 300,
      cell: (row: KnowledgeItem) => (
        <div>
          <Text strong>{row.title}</Text>
          <br />
          <Text type="secondary" size="small">{row.summary}</Text>
        </div>
      )
    },
    {
      title: '分类',
      colKey: 'category',
      width: 120,
      cell: (row: KnowledgeItem) => (
        <Tag theme="primary" variant="light">
          {categories.find(c => c.value === row.category)?.label || row.category}
        </Tag>
      )
    },
    {
      title: '来源',
      colKey: 'source',
      width: 120,
      cell: (row: KnowledgeItem) => <Text type="secondary">{row.source}</Text>
    },
    {
      title: '发布日期',
      colKey: 'publishDate',
      width: 100,
      cell: (row: KnowledgeItem) => <Text>{row.publishDate}</Text>
    },
    {
      title: '相关度',
      colKey: 'relevance',
      width: 100,
      cell: (row: KnowledgeItem) => (
        <Tag 
          theme={row.relevance >= 80 ? 'success' : row.relevance >= 60 ? 'warning' : 'danger'}
          variant="light"
        >
          {row.relevance}%
        </Tag>
      )
    },
    {
      title: '操作',
      colKey: 'actions',
      width: 120,
      cell: (row: KnowledgeItem) => (
        <Space size="small">
          <Button size="small" variant="text">查看</Button>
          <Button size="small" variant="text" icon={<DownloadIcon />}>下载</Button>
        </Space>
      )
    }
  ];

  const fetchKnowledgeData = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/v1/knowledge/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: searchQuery || '',
          category: selectedCategory !== 'all' ? selectedCategory : undefined,
          limit: 50
        })
      });

      if (!response.ok) {
        throw new Error('获取知识库数据失败');
      }

      const data = await response.json();
      setKnowledgeData(data.items || []);

    } catch (err) {
      setError(err instanceof Error ? err.message : '获取数据失败');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    fetchKnowledgeData();
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  useEffect(() => {
    // 初始加载数据
    fetchKnowledgeData();
  }, [selectedCategory]);

  return (
    <div style={{ padding: '24px', maxWidth: '1400px', margin: '0 auto' }}>
      <Title level={2}>金融知识库</Title>
      
      {/* 搜索和筛选区域 */}
      <Card>
        <Space size="large" align="center">
          <Input
            placeholder="搜索金融知识、研究报告、市场分析..."
            value={searchQuery}
            onChange={setSearchQuery}
            onKeyPress={handleKeyPress}
            style={{ width: '300px' }}
            prefix={<SearchIcon />}
          />
          
          <Space size="small">
            {categories.map(category => (
              <Button
                key={category.value}
                variant={selectedCategory === category.value ? 'base' : 'outline'}
                onClick={() => setSelectedCategory(category.value)}
              >
                {category.label}
              </Button>
            ))}
          </Space>

          <Button
            theme="primary"
            onClick={handleSearch}
            loading={loading}
          >
            搜索
          </Button>
        </Space>
      </Card>

      {error && (
        <Alert theme="error" style={{ marginTop: '16px' }}>
          {error}
        </Alert>
      )}

      {/* 知识库内容 */}
      <Card style={{ marginTop: '16px' }}>
        <Space size="middle" align="center" style={{ marginBottom: '16px' }}>
          <BookIcon />
          <Title level={4}>知识库内容</Title>
          <Text type="secondary">共 {knowledgeData.length} 条记录</Text>
        </Space>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '40px' }}>
            <Spin size="large" />
            <Text style={{ display: 'block', marginTop: '16px' }}>正在加载知识库数据...</Text>
          </div>
        ) : knowledgeData.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px', color: '#999' }}>
            <BookIcon style={{ fontSize: '48px', marginBottom: '16px' }} />
            <Text>暂无数据</Text>
            <br />
            <Text type="secondary">尝试搜索或选择其他分类</Text>
          </div>
        ) : (
          <Table
            data={knowledgeData}
            columns={columns}
            rowKey="id"
            size="medium"
            hover
            pagination={{
              defaultCurrent: 1,
              defaultPageSize: 20,
              total: knowledgeData.length,
              showJumper: true,
              showPageSize: true,
              pageSizeOptions: [10, 20, 50, 100]
            }}
          />
        )}
      </Card>

      {/* 热门标签 */}
      <Card style={{ marginTop: '16px' }}>
        <Title level={4}>热门标签</Title>
        <Space size="small" wrap>
          <Tag>财务报表分析</Tag>
          <Tag>宏观经济</Tag>
          <Tag>行业研究</Tag>
          <Tag>投资策略</Tag>
          <Tag>风险管理</Tag>
          <Tag>估值模型</Tag>
          <Tag>技术分析</Tag>
          <Tag>基本面分析</Tag>
          <Tag>市场趋势</Tag>
          <Tag>政策解读</Tag>
        </Space>
      </Card>

      {/* 数据统计 */}
      <Card style={{ marginTop: '16px' }}>
        <Title level={4}>知识库统计</Title>
        <Space size="large">
          <div style={{ textAlign: 'center' }}>
            <Title level={1} style={{ color: '#1890ff', margin: 0 }}>1,258</Title>
            <Text type="secondary">总文档数</Text>
          </div>
          <div style={{ textAlign: 'center' }}>
            <Title level={1} style={{ color: '#52c41a', margin: 0 }}>356</Title>
            <Text type="secondary">研究报告</Text>
          </div>
          <div style={{ textAlign: 'center' }}>
            <Title level={1} style={{ color: '#faad14', margin: 0 }}>892</Title>
            <Text type="secondary">财务数据</Text>
          </div>
          <div style={{ textAlign: 'center' }}>
            <Title level={1} style={{ color: '#f5222d', margin: 0 }}>3.2TB</Title>
            <Text type="secondary">数据总量</Text>
          </div>
        </Space>
      </Card>
    </div>
  );
};

export default KnowledgePage;