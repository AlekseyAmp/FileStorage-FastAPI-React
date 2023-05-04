import React, { useEffect, useState } from 'react';

import Cookie from 'js-cookie';
import axios from '../../utils/axios';

import styles from './Profile.module.scss';
import '../../assets/variables.scss';

function Profile() {
  const access_token = Cookie.get('access_token');

  const [email, setEmail] = useState()

  const [upload, setUpload] = useState()
  const [download, setDownload] = useState()
  const [deleted, setDeleted] = useState()

  useEffect(() => {
    async function getEmail() {
      try {
        const response = await axios.get(`/users/info`, {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });
        setEmail(response.data.email);
      } catch (error) {
        console.log(error.response.data.detail);
      }
    }
    getEmail();
  }, []);

  useEffect(() => {
    async function getStatisticAll() {
      try {
        const response = await axios.get(`/statistic`, {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });
        setUpload(response.data.upload);
        setDownload(response.data.download);
        setDeleted(response.data.deleted)
      } catch (error) {
        console.log(error.response.data.detail);
      }
    }
    getStatisticAll();
  }, []);

  return (
    <div className={styles.profile} >
      <div className={'title'}>Профиль и настройки</div>
      <div className={styles.profileContent}>
        <div className={styles.userInfo}>
          <div className={styles.userInfoAvatar}>
            <img src="../../img/avatar.png" alt="avatar" />
          </div>
          <div className={styles.userInfoChange}>
            <div className={styles.userInfoChangeElem}>
              <p className={`dark-text`}><span className={`bold-text`}>Почта:</span> {email}</p>
              <div className={`${styles.changeButton} link-text-orange`}>
                Изменить
              </div>

            </div>
          </div>
        </div>
        <div className={styles.statistic}>
          <h3 className={`bold-text`}>За все время, Вы:</h3>
          <div className={styles.statisticData}>
            <p className={`dark-text`}>Загрузили <span className={`bold-text`}>{upload}</span> файла(ов)</p>
            <p className={`dark-text`}>Скачали <span className={`bold-text`}>{download}</span> файла(ов)</p>
            <p className={`dark-text`}>Удалили <span className={`bold-text`}>{deleted}</span> файла(ов)</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Profile;