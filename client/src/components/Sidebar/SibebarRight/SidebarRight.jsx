import { React, useState, useEffect } from 'react';

import Cookie from 'js-cookie'
import axios from '../../../axios';

import styles from './SidebarRight.module.scss';
import '../../../assets/variables.scss';


function SidebarRight() {
  const username = Cookie.get('logged_in') === 'true' ? Cookie.get('email').slice(0, Cookie.get('email').indexOf('@')) : 'none'

  const access_token = Cookie.get('access_token')

  const [countFiles, setCountFiles] = useState(0)
  const [sizeFiles, setSizeFiles] = useState(0)

  useEffect(() => {
    async function getFilesInfo() {
      try {
        const response = await axios.get(`/files/info`, {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });
        setCountFiles(response.data.count);
        setSizeFiles(response.data.size)
      } catch (error) {
        console.log(error.response.data.detail);
      }
    }
    getFilesInfo();
  }, []);

  return (
    <div className={styles.sidebarRight}>
      <div className={styles.user}>
        <div onClick={() => (window.location.href = '/')} className={styles.userInfo} href="#">
          <img src="../img/avatar.png" alt="avatar" />
          <p className={`dark-text`}>{username}</p>
        </div>
        <div onClick={() => (window.location.href = '/')} className={styles.userNotifications} href="#">
          <img src="../img/sidebarRight/notification.png" alt="notification" />
        </div>
      </div>

      <div className={styles.todayStats}>
        <p className={`dark-text`}>Статистика за сегодня</p>
        <div className={styles.todayStatsContent}>
          <p className={`gray-text`}>Загружено файлов:</p>
          <p className={`gray-text`}>Скачано файлов:</p>
          <p className={`gray-text`}>Удалено файлов:</p>
        </div>
      </div>

      <div className={styles.diskSpace}>
        <p className={`dark-text`}>Общее количество файлов на диске: {countFiles}</p>
        <div className={styles.diskSpaceGraphic}>
          test
        </div>
        <p className={`small-text`}>Занято {sizeFiles} гб из 15 гб</p>
      </div>

      <div onClick={() => (window.location.href = '/')} className={styles.upgradeSpace}>
        <img src="../img/sidebarRight/premium.png" alt="premium" />
        <h3 className={`title`}>Купить больше места</h3>
      </div>
    </div>
  )
}

export default SidebarRight;
