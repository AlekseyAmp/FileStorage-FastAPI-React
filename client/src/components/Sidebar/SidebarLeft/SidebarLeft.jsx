import React from 'react';
import { Link } from 'react-router-dom';

import Cookie from 'js-cookie';
import axios from '../../../utils/axios';

import styles from './SidebarLeft.module.scss';
import '../../../assets/variables.scss';

import Logout from '../../../pages/Auth/Logout';

function SidebarLeft() {
  const access_token = Cookie.get('access_token');
  const category_name = 'default_category';

  async function uploadFile() {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.onchange = async () => {
      const file = fileInput.files[0];
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await axios.post(`/files/upload/${category_name}`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `Bearer ${access_token}`
          }
        });
        console.log(response);
      } catch (error) {
        console.log(error.response.data.detail);
      }
    };
    fileInput.click();
  }

  return (
    <div className={styles.sidebarLeft}>
      <Link to='/home' className={styles.logo}>
        <img src="../../img/sidebarLeft/logo.png" alt="Logo" />
        <h3 className={`title`}>CloudBox</h3>
      </Link>

      <div className={styles.uploadFile} onClick={uploadFile}>
        <p className={`dark-text`}>
          Загрузить <br /> файл
        </p>
        <img src="../../img/sidebarLeft/add.png" alt="Upload" />
      </div>

      <div className={styles.menu}>
        <ul>
          <li>
            <img src="../../img/sidebarLeft/favorite.png" alt="favorite" />
            <Link to='/favorite' className={`link-text`}>Избранное</Link>
          </li>

          <li>
            <img src="../../img/sidebarLeft/history.png" alt="history" />
            <Link to='/history' className={`link-text`}>История</Link>
          </li>

          <li>
            <img src="../../img/sidebarLeft/trash.png" alt="basket" />
            <Link to='/basket' className={`link-text`}>Корзина</Link>
          </li>
        </ul>
      </div>

      <div className={styles.menu}>
        <ul>
          <li>
            <img src="../../img/sidebarLeft/settings.png" alt="settings" />
            <Link to='/profile' className={`link-text`}>Настройки</Link>
          </li>

          <li>
            <img src="../../img/sidebarLeft/logout.png" alt="logout" />
            <Logout />
          </li>
        </ul>
      </div>

    </div>
  )
}

export default SidebarLeft;
