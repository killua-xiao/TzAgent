import { createBrowserRouter } from 'react-router-dom';
import Layout from '../components/Layout';
import Dashboard from '../pages/Dashboard';
import Analysis from '../pages/Analysis';
import KnowledgeBase from '../pages/KnowledgeBase';
import Chat from '../pages/Chat';
import Reports from '../pages/Reports';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      {
        index: true,
        element: <Dashboard />,
      },
      {
        path: 'dashboard',
        element: <Dashboard />,
      },
      {
        path: 'analysis',
        element: <Analysis />,
      },
      {
        path: 'knowledge',
        element: <KnowledgeBase />,
      },
      {
        path: 'chat',
        element: <Chat />,
      },
      {
        path: 'reports',
        element: <Reports />,
      },
    ],
  },
]);

export default router;