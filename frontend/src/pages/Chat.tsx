import React, { useState } from 'react';
import { Card, Input, Button, Space, Typography, Avatar } from 'tdesign-react';
import { UserIcon, RobotIcon } from 'tdesign-icons-react';

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');

  const handleSend = () => {
    if (inputValue.trim()) {
      const userMessage: Message = {
        id: Date.now().toString(),
        content: inputValue,
        sender: 'user',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, userMessage]);
      setInputValue('');

      // 模拟AI回复
      setTimeout(() => {
        const aiMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: '这是AI的回复，基于您的金融问题进行深度分析...',
          sender: 'ai',
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, aiMessage]);
      }, 1000);
    }
  };

  return (
    <div className="p-6 h-full">
      <Typography.Title level={2}>AI金融助手</Typography.Title>
      <Card className="h-[calc(100vh-200px)]">
        <div className="h-[calc(100%-80px)] overflow-y-auto mb-4">
          <Space direction="vertical" size="large" className="w-full">
            {messages.map(message => (
              <div
                key={message.id}
                className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`flex items-start max-w-2/3 ${message.sender === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                  <Avatar
                    icon={message.sender === 'user' ? <UserIcon /> : <RobotIcon />}
                    className={message.sender === 'user' ? 'ml-2' : 'mr-2'}
                  />
                  <div
                    className={`p-3 rounded-lg ${
                      message.sender === 'user'
                        ? 'bg-blue-100 text-blue-900'
                        : 'bg-gray-100 text-gray-900'
                    }`}
                  >
                    <Typography.Text>{message.content}</Typography.Text>
                    <div className="text-xs text-gray-500 mt-1">
                      {message.timestamp.toLocaleTimeString()}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </Space>
        </div>

        <Space size="small" className="w-full">
          <Input
            value={inputValue}
            onChange={setInputValue}
            placeholder="输入您的金融问题..."
            onEnter={handleSend}
            className="flex-1"
          />
          <Button onClick={handleSend}>发送</Button>
        </Space>
      </Card>
    </div>
  );
};

export default Chat;