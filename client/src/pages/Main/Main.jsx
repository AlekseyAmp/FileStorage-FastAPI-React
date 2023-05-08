import React from 'react';
import { Link } from 'react-router-dom';

import styles from './Main.module.scss';
import '../../assets/variables.scss';

import Button from '../../components/Button/Button';

function Main() { 

  return (
    <div className={styles.main}>
      <div className={'title'}>Добро пожаловать в CloudBox!</div>
      <div className={styles.mainContent}>
        <Link to="/register">
          <Button title={'Регистрация'} />
        </Link>
        <Link to="/login">
          <Button title={'Вход'} />
        </Link>
      </div>
    </div>
  );
}

export default Main;
