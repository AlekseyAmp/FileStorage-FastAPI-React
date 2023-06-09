import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom'

import Cookie from 'js-cookie'
import axios from '../../../utils/axios';
import formatFileSize from '../../../utils/formatFile';

import styles from './SidebarRight.module.scss';
import '../../../assets/variables.scss';


function SidebarRight() {
  const access_token = Cookie.get('access_token')

  const [username, setUsername] = useState()

  const [countFiles, setCountFiles] = useState()
  const [sizeFiles, setSizeFiles] = useState()

  const [uploadToday, setUploadToday] = useState()
  const [downloadToday, setDownloadToday] = useState()
  const [deletedToday, setDeletedToday] = useState()


  useEffect(() => {
    async function getUsername() {
      try {
        const response = await axios.get(`/users/info`, {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });
        setUsername(response.data.username);
      } catch (error) {
        console.log(error.response.data.detail);
      }
    }
    getUsername();
  }, []);
  
  useEffect(() => {
    async function getFilesInfo() {
      try {
        const response = await axios.get(`/files/info/total`, {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });
        setCountFiles(response.data.total_count);
        setSizeFiles(response.data.total_size);
      } catch (error) {
        console.log(error.response.data.detail);
      }
    }
    getFilesInfo();
  }, []);

  useEffect(() => {
    async function getStatisticToday() {
      try {
        const response = await axios.get(`/statistic/today`, {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });
        setUploadToday(response.data.upload);
        setDownloadToday(response.data.download);
        setDeletedToday(response.data.deleted)
      } catch (error) {
        console.log(error.response.data.detail);
      }
    }
    getStatisticToday();
  }, []);

  const progressWidth = Math.min((sizeFiles / (15 * 1024 ** 3)) * 100, 100);
  return (
    <div className={styles.sidebarRight}>
      <div className={styles.user}>
        <Link to='/profile' className={styles.userInfo}>
          <img src="../../img/avatar.png" alt="avatar" />
          <p className="dark-text">{username}</p>
        </Link>
        <div onClick={() => (window.location.href = '/')} className={styles.userNotifications} href="#">
          <img src="../../img/sidebarRight/notification.png" alt="notification" />
        </div>
      </div>

      <div className={styles.todayStats}>
        <p className={`dark-text`}>Статистика за сегодня</p>
        <div className={styles.todayStatsContent}>
          <p className={`gray-text`}>Загружено файлов: {uploadToday}</p>
          <p className={`gray-text`}>Скачано файлов: {downloadToday}</p>
          <p className={`gray-text`}>Удалено файлов: {deletedToday}</p>
        </div>
      </div>

      <div className={styles.diskSpace}>
        <p className={`dark-text`}>Общее количество файлов на диске: {countFiles}</p>
        <div className={styles.diskSpaceGraphic}>
          <div
            className={styles.diskSpaceProgress}
            style={{ width: `${progressWidth}%` }}
          />
        </div>
        <p style={{ marginTop: '10px' }} className={`small-text`}>
          Занято {formatFileSize(sizeFiles)} гб из 15 гб
        </p>
      </div>


      <div onClick={() => (window.location.href = '/')} className={styles.upgradeSpace}>
        <img src="../../img/sidebarRight/premium.png" alt="premium" />
        <h3 className={`title`}>Купить больше места</h3>
      </div>
    </div>
  )
}

export default SidebarRight;
