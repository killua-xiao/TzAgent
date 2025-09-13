import React, { useState, useEffect } from 'react';
import { 
  Table, 
  Input, 
  Button, 
  Select, 
  DatePicker, 
  Message, 
  Pagination,
  Loading,
  Card,
  Space,
  Form,
  Tag,
  Dialog,
  Divider,
  Alert
} from 'tdesign-react';
import { 
  SearchIcon, 
  AddIcon, 
  RefreshIcon, 
  ChartIcon, 
  SettingIcon
} from 'tdesign-icons-react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { fetchStocks, createStock, stockApi } from '../services/api';
import type { StockData, CreateStockRequest } from '../types';
import type { PaginationProps } from 'tdesign-react/es/pagination';
import type { TableRowData } from 'tdesign-react/es/table/type';
import StockChart from './StockChart';

// 定义表格列
const columns = [
  {
    title: '股票代码',
    colKey: 'symbol',
    width: 120,
    fixed: 'left',
  },
  {
    title: '股票名称',
    colKey: 'name',
    width: 150,
  },
  {
    title: '当前价格',
    colKey: 'price',
    width: 120,
    cell: (row: StockData) => `¥${row.price.toFixed(2)}`,
  },
  {
    title: '涨跌幅',
    colKey: 'changePercent',
    width: 120,
    cell: (row: StockData) => (
      <Tag 
        theme={row.changePercent >= 0 ? 'success' : 'danger'}
        variant="light"
      >
        {row.changePercent >= 0 ? '+' : ''}{row.changePercent.toFixed(2)}%
      </Tag>
    ),
  },
  {
    title: '市值',
    colKey: 'marketCap',
    width: 150,
    cell: (row: StockData) => {
      const cap = row.marketCap;
      if (cap >= 1e12) return `¥${(cap / 1e12).toFixed(2)}万亿`;
      if (cap >= 1e8) return `¥${(cap / 1e8).toFixed(2)}亿`;
      return `¥${(cap / 1e4).toFixed(2)}万`;
    },
  },
  {
    title: '行业',
    colKey: 'industry',
    width: 120,
  },
  {
    title: '更新时间',
    colKey: 'updateTime',
    width: 180,
    cell: (row: StockData) => new Date(row.updateTime).toLocaleString(),
  },
  {
    title: '操作',
    colKey: 'operations',
    width: 120,
    fixed: 'right',
    cell: () => (
      <Space size="small">
        <Button theme="primary" variant="text" size="small">
          分析
        </Button>
        <Button theme="default" variant="text" size="small">
          详情
        </Button>
      </Space>
    ),
  },
];

// 筛选表单类型
interface FilterForm {
  symbol?: string;
  name?: string;
  industry?: string;
  minPrice?: number;
  maxPrice?: number;
  startDate?: Date;
  endDate?: Date;
}

// 分页参数类型
interface PaginationParams {
  current: number;
  pageSize: number;
}

const DataTableWithFilter: React.FC = () => {
  // 状态管理
  const [filterForm, setFilterForm] = useState<FilterForm>({});
  const [pagination, setPagination] = useState<PaginationParams>({
    current: 1,
    pageSize: 10,
  });
  const [selectedRows, setSelectedRows] = useState<StockData[]>([]);
  const [isCreateModalVisible, setIsCreateModalVisible] = useState(false);
  const [isTestModalVisible, setIsTestModalVisible] = useState(false);
  const [isChartModalVisible, setIsChartModalVisible] = useState(false);
  const [selectedStock, setSelectedStock] = useState<StockData | null>(null);
  const [apiTestResult, setApiTestResult] = useState<string>('');
  const [isTesting, setIsTesting] = useState(false);
  const [createForm] = Form.useForm();
  const queryClient = useQueryClient();

  // 查询数据
  const {
    data: stockData,
    isLoading,
    error,
    refetch,
  } = useQuery(
    ['stocks', filterForm, pagination],
    () => fetchStocks({
      ...filterForm,
      page: pagination.current,
      page_size: pagination.pageSize,
    }),
    {
      keepPreviousData: true,
      staleTime: 5 * 60 * 1000, // 5分钟缓存
    }
  );

  // 创建股票的mutation
  const createMutation = useMutation(createStock, {
    onSuccess: () => {
      showMessage('success', '股票数据创建成功');
      setIsCreateModalVisible(false);
      createForm.reset();
      refetch();
    },
    onError: (error: Error) => {
      showMessage('error', `创建失败: ${error.message}`);
    },
  });

  // 处理筛选表单变化
  const handleFilterChange = (key: keyof FilterForm, value: any) => {
    setFilterForm(prev => ({
      ...prev,
      [key]: value,
    }));
  };

  // 处理分页变化
  const handlePageChange: PaginationProps['onChange'] = (pageInfo) => {
    setPagination({
      current: pageInfo.current,
      pageSize: pageInfo.pageSize,
    });
  };

  // 处理行选择
  const handleSelectChange = (selectedRowKeys: Array<string | number>, options: { selectedRowData: TableRowData[] }) => {
    setSelectedRows(options.selectedRowData as StockData[]);
  };

  // 显示消息提示
  const showMessage = (type: 'success' | 'error' | 'info', content: string) => {
    if (type === 'success') {
      Message.success(content, 3000);
    } else if (type === 'error') {
      Message.error(content, 3000);
    } else {
      Message.info(content, 3000);
    }
  };

  // 处理表单提交
  const handleCreateSubmit = async (formData: CreateStockRequest) => {
    try {
      await createMutation.mutateAsync(formData);
    } catch (err) {
      console.error('创建股票失败:', err);
    }
  };

  // 处理搜索
  const handleSearch = () => {
    setPagination(prev => ({ ...prev, current: 1 }));
    refetch();
  };

  // 处理重置
  const handleReset = () => {
    setFilterForm({});
    setPagination({ current: 1, pageSize: 10 });
  };

  // 显示错误信息
  useEffect(() => {
    if (error) {
      showMessage('error', `数据加载失败: ${error.message}`);
    }
  }, [error]);

  // API连接测试
  const testApiConnection = async () => {
    setIsTesting(true);
    setApiTestResult('');
    try {
      const response = await stockApi.getStocks({ page: 1, pageSize: 1 });
      setApiTestResult(`✅ API连接成功！获取到 ${response.data?.data?.length || 0} 条数据`);
      showMessage('success', 'API连接测试成功');
    } catch (err: any) {
      setApiTestResult(`❌ API连接失败: ${err.message}`);
      showMessage('error', 'API连接测试失败');
    } finally {
      setIsTesting(false);
    }
  };

  // 查看股票图表
  const handleViewChart = (stock: StockData) => {
    setSelectedStock(stock);
    setIsChartModalVisible(true);
  };

  // 刷新数据
  const handleRefreshData = () => {
    queryClient.invalidateQueries(['stocks']);
    showMessage('success', '数据已刷新');
  };

  return (
    <Card title="股票数据管理" className="w-full">
      {/* 筛选表单 */}
      <div className="p-4 bg-gray-50 rounded-lg mb-4">
        <Space size="large" align="start">
          <Form layout="inline" className="flex-1">
            <Form.Item label="股票代码">
              <Input
                placeholder="输入股票代码"
                value={filterForm.symbol || ''}
                onChange={(value) => handleFilterChange('symbol', value)}
                clearable
              />
            </Form.Item>
            
            <Form.Item label="股票名称">
              <Input
                placeholder="输入股票名称"
                value={filterForm.name || ''}
                onChange={(value) => handleFilterChange('name', value)}
                clearable
              />
            </Form.Item>
            
            <Form.Item label="行业">
              <Select
                placeholder="选择行业"
                value={filterForm.industry}
                onChange={(value) => handleFilterChange('industry', value)}
                clearable
                options={[
                  { label: '科技', value: 'technology' },
                  { label: '金融', value: 'finance' },
                  { label: '医疗', value: 'healthcare' },
                  { label: '消费', value: 'consumer' },
                  { label: '能源', value: 'energy' },
                ]}
              />
            </Form.Item>
            
            <Form.Item label="价格区间">
              <Space size="small">
                <Input
                  placeholder="最低价"
                  type="number"
                  value={filterForm.minPrice?.toString() || ''}
                  onChange={(value) => handleFilterChange('minPrice', value ? Number(value) : undefined)}
                  clearable
                />
                <span className="text-gray-400">-</span>
                <Input
                  placeholder="最高价"
                  type="number"
                  value={filterForm.maxPrice?.toString() || ''}
                  onChange={(value) => handleFilterChange('maxPrice', value ? Number(value) : undefined)}
                  clearable
                />
              </Space>
            </Form.Item>
          </Form>
          
          <Space direction="vertical" size="small">
            <Button
              theme="primary"
              icon={<SearchIcon />}
              onClick={handleSearch}
              loading={isLoading}
            >
              搜索
            </Button>
            <Button
              theme="default"
              icon={<RefreshIcon />}
              onClick={handleReset}
              disabled={isLoading}
            >
              重置
            </Button>
          </Space>
        </Space>
      </div>

      {/* 操作栏 */}
      <div className="flex justify-between items-center mb-4">
        <Space>
          <Button
            theme="primary"
            icon={<AddIcon />}
            onClick={() => setIsCreateModalVisible(true)}
          >
            新增股票
          </Button>
          <Button
            theme="default"
            disabled={selectedRows.length === 0}
            onClick={() => Message.info(`已选择 ${selectedRows.length} 条数据`)}
          >
            批量操作
          </Button>
          <Button
            theme="warning"
            icon={<ChartIcon />}
            onClick={() => {
              setIsTestModalVisible(true);
              testApiConnection();
            }}
            loading={isTesting}
          >
            API测试
          </Button>
          <Button
            theme="success"
            icon={<RefreshIcon />}
            onClick={handleRefreshData}
            loading={isLoading}
          >
            刷新数据
          </Button>
        </Space>
        
        <div className="text-sm text-gray-500">
          共 {stockData?.total || 0} 条数据
        </div>
      </div>

      {/* 数据表格 */}
      <Spin loading={isLoading} showOverlay>
        <Table
          columns={columns}
          data={stockData?.data || []}
          rowKey="id"
          selectOnRowClick
          selectedRowKeys={selectedRows.map(row => row.id)}
          onSelectChange={handleSelectChange}
          pagination={false}
          size="medium"
          hover
          stripe
          verticalAlign="middle"
          className="min-h-400"
        />
      </Spin>

      {/* 分页 */}
      {stockData && stockData.total > 0 && (
        <div className="flex justify-center mt-4">
          <Pagination
            total={stockData.total}
            current={pagination.current}
            pageSize={pagination.pageSize}
            onChange={handlePageChange}
            showJumper
            showPageSize
            pageSizeOptions={[10, 20, 50, 100]}
          />
        </div>
      )}

      {/* 空状态 */}
      {!isLoading && (!stockData || stockData.data.length === 0) && (
        <div className="text-center py-12 text-gray-400">
          <div className="text-4xl mb-2">📊</div>
          <div className="text-lg">暂无数据</div>
          <div className="text-sm mt-1">尝试调整搜索条件或添加新数据</div>
        </div>
      )}

      {/* 创建模态框 */}
      <Form.Modal
        visible={isCreateModalVisible}
        onClose={() => setIsCreateModalVisible(false)}
        onSubmit={handleCreateSubmit}
        form={createForm}
        title="新增股票数据"
        confirmLoading={createMutation.isLoading}
        width={600}
      >
        <Form form={createForm} labelWidth={100} layout="vertical">
          <Form.Item
            name="symbol"
            label="股票代码"
            rules={[{ required: true, message: '请输入股票代码' }]}
          >
            <Input placeholder="例如：000001" />
          </Form.Item>
          
          <Form.Item
            name="name"
            label="股票名称"
            rules={[{ required: true, message: '请输入股票名称' }]}
          >
            <Input placeholder="例如：平安银行" />
          </Form.Item>
          
          <Form.Item
            name="price"
            label="当前价格"
            rules={[
              { required: true, message: '请输入价格' },
              { pattern: /^\d+(\.\d{1,2})?$/, message: '请输入有效的价格格式' }
            ]}
          >
            <Input type="number" step="0.01" placeholder="例如：15.68" />
          </Form.Item>
          
          <Form.Item
            name="industry"
            label="行业分类"
            rules={[{ required: true, message: '请选择行业' }]}
          >
            <Select
              options={[
                { label: '科技', value: 'technology' },
                { label: '金融', value: 'finance' },
                { label: '医疗', value: 'healthcare' },
                { label: '消费', value: 'consumer' },
                { label: '能源', value: 'energy' },
              ]}
              placeholder="请选择行业"
            />
          </Form.Item>
          
          <Form.Item
            name="marketCap"
            label="市值（亿元）"
            rules={[
              { required: true, message: '请输入市值' },
              { pattern: /^\d+(\.\d{1,2})?$/, message: '请输入有效的市值格式' }
            ]}
          >
            <Input type="number" step="0.01" placeholder="例如：1500.50" />
          </Form.Item>
        </Form>
      </Form.Modal>

      {/* API测试模态框 */}
      <Modal
        header="API连接测试"
        visible={isTestModalVisible}
        onClose={() => setIsTestModalVisible(false)}
        footer={
          <Space>
            <Button onClick={() => setIsTestModalVisible(false)}>关闭</Button>
            <Button theme="primary" onClick={testApiConnection}>
              重新测试
            </Button>
          </Space>
        }
      >
        {isTesting ? (
          <div className="flex items-center justify-center py-8">
            <Spin size="large" text="测试API连接中..." />
          </div>
        ) : (
          <div className="space-y-4">
            <div className={`p-4 rounded ${
              apiTestResult.includes('✅') 
                ? 'bg-green-50 text-green-700 border border-green-200' 
                : 'bg-red-50 text-red-700 border border-red-200'
            }`}>
              <div className="font-medium">
                {apiTestResult.includes('✅') ? '✅ API连接成功' : '❌ API连接失败'}
              </div>
              <div className="text-sm mt-1">{apiTestResult}</div>
            </div>
            <div className="text-xs text-gray-500">
              测试时间: {new Date().toLocaleString()}
            </div>
          </div>
        )}
      </Modal>

      {/* 图表展示模态框 */}
      <Modal
        header="股票图表分析"
        visible={isChartModalVisible}
        onClose={() => setIsChartModalVisible(false)}
        footer={
          <Button onClick={() => setIsChartModalVisible(false)}>关闭</Button>
        }
        width="90%"
        style={{ maxWidth: '1200px' }}
      >
        {selectedStock && (
          <div className="h-96">
            <StockChart symbol={selectedStock.symbol} period="1m" />
          </div>
        )}
      </Modal>
    </Card>
  );
};

export default DataTableWithFilter;