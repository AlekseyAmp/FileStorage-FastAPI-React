import { React, useState, useEffect } from 'react';
import styles from './SidebarRight.module.scss';
import '../../../assets/variables.scss';
import Cookie from 'js-cookie'
import { useNavigate } from 'react-router-dom';

function SidebarRight() {
  const username = Cookie.get('logged_in') === 'true' ? Cookie.get('email').slice(0, Cookie.get('email').indexOf('@')) : 'none'
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
        <p className={`dark-text`}>Общее количество файлов на диске: N</p>
        <div className={styles.diskSpaceGraphic}>
          test
        </div>
        <p className={`small-text`}>Занято 0 гб из 15 гб</p>
      </div>

      <div onClick={() => (window.location.href = '/')} className={styles.upgradeSpace}>
        <img src="../img/sidebarRight/premium.png" alt="premium" />
        <h3 className={`title`}>Купить больше места</h3>
      </div>
    </div>
  )
}

export default SidebarRight;
