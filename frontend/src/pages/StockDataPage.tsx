import React from 'react';
import { Layout, Card } from 'tdesign-react';
import DataTableWithFilter from '../components/DataTableWithFilter';

const { Content } = Layout;

const StockDataPage: React.FC = () => {
  return (
    <Layout className="min-h-screen bg-gray-50">
      <Content className="p-6">
        <div className="max-w-7xl mx-auto">
          <Card className="shadow-lg rounded-lg">
            <DataTableWithFilter />
          </Card>
        </div>
      </Content>
    </Layout>
  );
};

export default StockDataPage;