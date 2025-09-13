import React from 'react';
import { Card, Typography, Input, Button, Space } from 'tdesign-react';

const KnowledgeBase: React.FC = () => {
  return (
    <div className="p-6">
      <Typography.Title level={2}>金融知识库</Typography.Title>
      <Space direction="vertical" size="large" className="w-full">
        <Card title="知识检索" bordered>
          <Space size="small" className="w-full">
            <Input placeholder="输入金融知识关键词..." className="flex-1" />
            <Button type="submit">搜索</Button>
          </Space>
        </Card>
        <Card title="知识分类" bordered>
          <div className="grid grid-cols-3 gap-4">
            <Card bordered hoverShadow>
              <Typography.Title level={4}>股票分析</Typography.Title>
              <Typography.Text>基本面、技术面、估值分析</Typography.Text>
            </Card>
            <Card bordered hoverShadow>
              <Typography.Title level={4}>宏观经济</Typography.Title>
              <Typography.Text>GDP、CPI、利率政策</Typography.Text>
            </Card>
            <Card bordered hoverShadow>
              <Typography.Title level={4}>行业研究</Typography.Title>
              <Typography.Text>行业趋势、竞争格局</Typography.Text>
            </Card>
          </div>
        </Card>
      </Space>
    </div>
  );
};

export default KnowledgeBase;