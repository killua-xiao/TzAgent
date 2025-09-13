import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Layout, Menu, Button, Avatar, Space, Typography } from 'tdesign-react';
import { 
  HomeIcon, 
  ChartIcon, 
  BookIcon, 
  ChatIcon, 
  UserIcon,
  MenuFoldIcon,
  MenuUnfoldIcon
} from 'tdesign-icons-react';

const { Header, Sider, Content } = Layout;
const { Title } = Typography;

interface LayoutProps {
  children: React.ReactNode;
}

const AppLayout: React.FC<LayoutProps> = ({ children }) => {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    {
      value: '/dashboard',
      label: '仪表盘',
      icon: <HomeIcon />,
    },
    {
      value: '/analysis',
      label: '股票分析',
      icon: <ChartIcon />,
    },
    {
      value: '/knowledge',
      label: '知识库',
      icon: <BookIcon />,
    },
    {
      value: '/chat',
      label: 'AI对话',
      icon: <ChatIcon />,
    },
  ];

  const handleMenuClick = (path: string) => {
    navigate(path);
  };

  return (
    <Layout className="h-screen">
      <Sider
        collapsed={collapsed}
        onCollapse={setCollapsed}
        style={{
          overflow: 'auto',
          height: '100vh',
          position: 'fixed',
          left: 0,
        }}
      >
        <div className="p-4 flex items-center justify-between border-b border-gray-200">
          {!collapsed && (
            <Title level={4} className="text-blue-600 m-0">
              金融AI助手
            </Title>
          )}
          <Button
            variant="text"
            icon={collapsed ? <MenuUnfoldIcon /> : <MenuFoldIcon />}
            onClick={() => setCollapsed(!collapsed)}
          />
        </div>
        
        <Menu
          value={location.pathname}
          onChange={handleMenuClick}
          style={{ border: 'none' }}
        >
          {menuItems.map(item => (
            <Menu.MenuItem
              key={item.value}
              value={item.value}
              icon={item.icon}
            >
              {!collapsed && item.label}
            </Menu.MenuItem>
          ))}
        </Menu>
      </Sider>

      <Layout style={{ marginLeft: collapsed ? 80 : 200, transition: 'margin-left 0.2s' }}>
        <Header className="bg-white border-b border-gray-200 px-6">
          <div className="flex justify-between items-center h-full">
            <div>
              <Title level={3} className="m-0">
                {menuItems.find(item => item.value === location.pathname)?.label || '金融AI助手'}
              </Title>
            </div>
            <Space>
              <Button variant="text">通知</Button>
              <Avatar icon={<UserIcon />} />
              <span className="text-gray-600">管理员</span>
            </Space>
          </div>
        </Header>

        <Content style={{ margin: '24px 16px 0', overflow: 'initial' }}>
          <div className="bg-white p-6 min-h-[calc(100vh-120px)]">
            {children}
          </div>
        </Content>
      </Layout>
    </Layout>
  );
};

export default AppLayout;