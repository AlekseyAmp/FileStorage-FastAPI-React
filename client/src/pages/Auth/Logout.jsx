import React from 'react';
import useNavigate from 'react-router-dom';

import axios from '../../axios';
import Cookie from 'js-cookie';

function Logout() {
  const navigate = useNavigate();

  async function handleSubmit() {
    try {
      const response = await axios.get('/auth/logout');

      if (response.data.status === 'success') {
        Cookie.remove('access_token');
        Cookie.remove('refresh_token');
        Cookie.remove('email');
        Cookie.set('logged_in', false);
        navigate('/login');
      }
    } catch (error) {
      console.log(error.response.data.detail);
    }
  };

  return (
    <a onClick={handleSubmit} className={"red-text"}>Выйти</a>
  );
}

export default Logout;
