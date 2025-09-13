import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Analysis from './pages/Analysis';
import KnowledgeBase from './pages/KnowledgeBase';
import Chat from './pages/Chat';
import './index.css';

const App: React.FC = () => {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/analysis" element={<Analysis />} />
          <Route path="/knowledge" element={<KnowledgeBase />} />
          <Route path="/chat" element={<Chat />} />
        </Routes>
      </Layout>
    </Router>
  );
};

export default App;