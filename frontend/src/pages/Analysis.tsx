import React from 'react';
import { Card, Typography, Space, Tabs } from 'tdesign-react';
import DataTableWithFilter from '../components/DataTableWithFilter';
import StockChart from '../components/StockChart';

const Analysis: React.FC = () => {
  return (
    <div className="p-6">
      <Typography.Title level="h2">金融数据分析</Typography.Title>
      
      <Tabs defaultValue="stocks" placement="top" size="large">
        <Tabs.TabPanel value="stocks" label="股票数据">
          <Card bordered={false} className="mt-4">
            <DataTableWithFilter />
          </Card>
        </Tabs.TabPanel>
        
        <Tabs.TabPanel value="technical" label="技术分析">
          <Space direction="vertical" size="large" className="w-full mt-4">
            <Card title="技术指标分析" bordered>
              <div className="h-96">
                <StockChart symbol="000001" period="1y" />
              </div>
            </Card>
            <Card title="技术指标配置" bordered>
              <div className="h-64 bg-gray-50 rounded flex items-center justify-center">
                <Typography.Text>技术指标配置区域</Typography.Text>
              </div>
            </Card>
          </Space>
        </Tabs.TabPanel>
        
        <Tabs.TabPanel value="fundamental" label="基本面分析">
          <Space direction="vertical" size="large" className="w-full mt-4">
            <Card title="财务数据分析" bordered>
              <div className="h-96 bg-gray-50 rounded flex items-center justify-center">
                <Typography.Text>财务数据图表区域</Typography.Text>
              </div>
            </Card>
            <Card title="估值分析" bordered>
              <div className="h-64 bg-gray-50 rounded flex items-center justify-center">
                <Typography.Text>估值分析配置区域</Typography.Text>
              </div>
            </Card>
          </Space>
        </Tabs.TabPanel>
        
        <Tabs.TabPanel value="reports" label="分析报告">
          <Card bordered={false} className="mt-4">
            <div className="h-96 bg-gray-50 rounded flex items-center justify-center">
              <Typography.Text>分析报告生成和管理区域</Typography.Text>
            </div>
          </Card>
        </Tabs.TabPanel>
      </Tabs>
    </div>
  );
};

export default Analysis;