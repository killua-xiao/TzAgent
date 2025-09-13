import React, { useState, useRef, useEffect } from 'react';
import { Card, Input, Button, Space, Typography, Avatar, List, Spin } from 'tdesign-react';
import { SendIcon, UserIcon, RobotIcon } from 'tdesign-icons-react';

const { Title, Text } = Typography;

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
}

const ChatPage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputMessage,
      role: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await fetch('/api/v1/chat/message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          history: messages.slice(-10).map(m => ({
            role: m.role,
            content: m.content
          }))
        })
      });

      if (!response.ok) {
        throw new Error('发送消息失败');
      }

      const data = await response.json();
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: data.response,
        role: 'assistant',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: '抱歉，发送消息时出现错误，请稍后重试。',
        role: 'assistant',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const renderMessage = (message: Message) => (
    <div
      key={message.id}
      style={{
        display: 'flex',
        flexDirection: message.role === 'user' ? 'row-reverse' : 'row',
        marginBottom: '16px',
        alignItems: 'flex-start'
      }}
    >
      <Avatar
        icon={message.role === 'user' ? <UserIcon /> : <RobotIcon />}
        style={{
          backgroundColor: message.role === 'user' ? '#1890ff' : '#52c41a',
          margin: message.role === 'user' ? '0 0 0 12px' : '0 12px 0 0'
        }}
      />
      
      <Card
        style={{
          maxWidth: '70%',
          backgroundColor: message.role === 'user' ? '#e6f7ff' : '#f6ffed',
          border: '1px solid #d9d9d9'
        }}
      >
        <Text>{message.content}</Text>
        <br />
        <Text type="secondary" style={{ fontSize: '12px' }}>
          {message.timestamp.toLocaleTimeString()}
        </Text>
      </Card>
    </div>
  );

  return (
    <div style={{ padding: '24px', maxWidth: '800px', margin: '0 auto', height: '100vh' }}>
      <Title level={2}>智能投研助手</Title>
      
      <Card style={{ height: 'calc(100vh - 200px)', display: 'flex', flexDirection: 'column' }}>
        {/* 消息列表 */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '16px' }}>
          {messages.length === 0 ? (
            <div style={{ textAlign: 'center', color: '#999', padding: '40px' }}>
              <RobotIcon style={{ fontSize: '48px', marginBottom: '16px' }} />
              <Text>我是您的智能投研助手，请问有什么可以帮您？</Text>
              <br />
              <Text type="secondary">例如：分析AAPL的财务数据、比较TSLA和NIO的技术指标等</Text>
            </div>
          ) : (
            messages.map(renderMessage)
          )}
          
          {loading && (
            <div style={{ display: 'flex', alignItems: 'flex-start', marginBottom: '16px' }}>
              <Avatar icon={<RobotIcon />} style={{ backgroundColor: '#52c41a', margin: '0 12px 0 0' }} />
              <Card style={{ backgroundColor: '#f6ffed', border: '1px solid #d9d9d9' }}>
                <Space size="small">
                  <Spin size="small" />
                  <Text>思考中...</Text>
                </Space>
              </Card>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* 输入区域 */}
        <div style={{ padding: '16px', borderTop: '1px solid #d9d9d9' }}>
          <Space size="middle" style={{ width: '100%' }}>
            <Input
              value={inputMessage}
              onChange={setInputMessage}
              onKeyPress={handleKeyPress}
              placeholder="输入您的问题..."
              style={{ flex: 1 }}
              disabled={loading}
            />
            <Button
              icon={<SendIcon />}
              theme="primary"
              onClick={handleSendMessage}
              loading={loading}
              disabled={!inputMessage.trim() || loading}
            >
              发送
            </Button>
          </Space>
        </div>
      </Card>
    </div>
  );
};

export default ChatPage;