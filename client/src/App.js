import React from 'react';
import { Routes, Route } from 'react-router-dom';
import routes from './routes';

import './assets/reset.scss';
import './assets/global.scss';

import SidebarLayout from './components/Sidebar/SidebarLayout';
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import Main from './pages/Main/Main';
import Category from './components/Category/Category';

import AuthChecked from './components/AuthChecked';

function App() {
  return (
    <div className="container">
      <Routes>
        <Route path="/login" element={<AuthChecked><Login /></AuthChecked>} />
        <Route path="/register" element={<AuthChecked><Register /></AuthChecked>} />
        <Route path="/" element={<AuthChecked><Main /></AuthChecked>} />
        {routes.map((route) => (
          <Route
            key={route.path}
            path={route.path}
            element={<AuthChecked><SidebarLayout><route.component /></SidebarLayout></AuthChecked>}
          />
        ))}
      </Routes>
    </div>
  );
}

export default App;
