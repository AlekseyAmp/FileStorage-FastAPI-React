import React from 'react';
import axios from '../../axios';
import Cookie from 'js-cookie';
import { useNavigate } from 'react-router-dom';
import styles from './Auth.module.scss'


function Logout() {
  const navigate = useNavigate();

  const handleSubmit = async () => {
    try {
      const access_token = Cookie.get('access_token');
      const headers = { Authorization: `Bearer ${access_token}` };
      const response = await axios.get('/logout', { headers });

      if (response.data.status === 'success') {
        Cookie.remove('access_token');
        Cookie.remove('refresh_token');
        Cookie.set('logged_in', 'false');

        navigate('/login');
      }
    } catch (error) {
      console.error(error.response.data.detail);
    }
  };

  return (
    <a onClick={handleSubmit} className={"red-text"}>Выйти</a>
  );
}

export default Logout;
