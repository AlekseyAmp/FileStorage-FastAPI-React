import React from 'react'
import Link from 'react-router-dom'

import styles from './SidebarLeft.module.scss';
import '../../../assets/variables.scss';

import Logout from '../../../pages/Auth/Logout';

function SidebarLeft() {

  const uploadFile = () => {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.click();
  }

  return (
    <div className={styles.sidebarLeft}>
      <Link to='/home' className={styles.logo}>
        <img src="../img/sidebarLeft/logo.png" alt="Logo" />
        <h3 className={`title`}>CloudBox</h3>
      </Link>

      <div className={styles.uploadFile} onClick={uploadFile}>
        <p className={`dark-text`}>
          Загрузить <br /> файл
        </p>
        <img src="../img/sidebarLeft/add.png" alt="Upload" />
      </div>

      <div className={styles.menu}>
        <ul>
          <li>
            <img src="../img/sidebarLeft/favorite.png" alt="favorite" />
            <Link to='/favorite' className={`link-text`}>Избранное</Link>
          </li>

          <li>
            <img src="../img/sidebarLeft/history.png" alt="history" />
            <Link to='/history' className={`link-text`}>История</Link>
          </li>

          <li>
            <img src="../img/sidebarLeft/trash.png" alt="basket" />
            <Link to='/basket' className={`link-text`}>Корзина</Link>
          </li>
        </ul>
      </div>

      <div className={styles.menu}>
        <ul>
          <li>
            <img src="../img/sidebarLeft/settings.png" alt="settings" />
            <a className={`link-text`} href="">Настройки</a>
          </li>

          <li>
            <img src="../img/sidebarLeft/logout.png" alt="logout" />
            <Logout />
          </li>
        </ul>
      </div>

    </div>
  )
}

export default SidebarLeft
