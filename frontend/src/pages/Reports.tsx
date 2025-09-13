import React from 'react';
import { Card, Typography, Button, Space, Table } from 'tdesign-react';
import { DownloadIcon, EyeIcon } from 'tdesign-icons-react';

interface Report {
  id: string;
  title: string;
  type: string;
  date: string;
  status: string;
}

const Reports: React.FC = () => {
  const reports: Report[] = [
    {
      id: '1',
      title: '腾讯控股基本面分析报告',
      type: '基本面分析',
      date: '2024-03-15',
      status: '已完成',
    },
    {
      id: '2',
      title: '贵州茅台技术面分析',
      type: '技术面分析',
      date: '2024-03-14',
      status: '已完成',
    },
    {
      id: '3',
      title: '新能源行业深度研究报告',
      type: '行业研究',
      date: '2024-03-13',
      status: '生成中',
    },
  ];

  const columns = [
    {
      title: '报告标题',
      colKey: 'title',
      width: 200,
    },
    {
      title: '类型',
      colKey: 'type',
      width: 120,
    },
    {
      title: '生成日期',
      colKey: 'date',
      width: 120,
    },
    {
      title: '状态',
      colKey: 'status',
      width: 100,
      cell: (row: any) => (
        <span
          className={`px-2 py-1 rounded text-xs ${
            row.status === '已完成' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'
          }`}
        >
          {row.status}
        </span>
      ),
    },
    {
      title: '操作',
      colKey: 'actions',
      width: 150,
      cell: () => (
        <Space size="small">
          <Button variant="text" icon={<EyeIcon />} size="small">
            查看
          </Button>
          <Button variant="text" icon={<DownloadIcon />} size="small">
            下载
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <Typography.Title level={2}>分析报告</Typography.Title>
        <Button>生成新报告</Button>
      </div>

      <Card>
        <Table
          data={reports}
          columns={columns}
          rowKey="id"
          size="medium"
          hover
          pagination={{
            defaultCurrent: 1,
            defaultPageSize: 10,
            total: reports.length,
          }}
        />
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
        <Card title="报告统计" bordered>
          <Space direction="vertical" size="large" className="w-full">
            <div className="flex justify-between">
              <Typography.Text>总报告数</Typography.Text>
              <Typography.Text strong>23</Typography.Text>
            </div>
            <div className="flex justify-between">
              <Typography.Text>本月生成</Typography.Text>
              <Typography.Text strong>8</Typography.Text>
            </div>
            <div className="flex justify-between">
              <Typography.Text>完成率</Typography.Text>
              <Typography.Text strong>92%</Typography.Text>
            </div>
          </Space>
        </Card>

        <Card title="快速生成" bordered>
          <Space direction="vertical" size="middle" className="w-full">
            <Button block>基本面分析报告</Button>
            <Button block>技术面分析报告</Button>
            <Button block>行业研究报告</Button>
          </Space>
        </Card>
      </div>
    </div>
  );
};

export default Reports;