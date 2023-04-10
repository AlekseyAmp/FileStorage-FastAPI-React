import React from 'react'
import { Link } from 'react-router-dom'

import styles from './AuthForm.module.scss'
import '../../assets/variables.scss'

import Input from '../Input/Input'
import Button from '../Button/Button'


const AuthForm = ({ inputConfigs, buttonTitle, authHelpText, authHelpLink, link, onSubmit }) => {
  return (
    <form className={styles.authForm} onSubmit={onSubmit}>
      {inputConfigs.map((inputConfig, index) => (
        <Input
          key={index}
          title={inputConfig.title}
          type={inputConfig.type}
          name={inputConfig.name}
        />
      ))}
      <Button type='submit' title={buttonTitle} marginTop={30} />
      <div className={styles.authHelp}>
        <p className={`dark-text`}>{authHelpText}</p>
        <Link to={link} className={`link-text-blue`}>{authHelpLink}</Link>
      </div>
    </form>
  );
};

export default AuthForm;
