import React from 'react'

import styles from './Input.module.scss'

function Input({title, placeholder, type, name}) {
  return (
    <div className={styles.inputForm}>
      <label htmlFor={name} className={`dark-text`}>{title}</label>
      <input type={type} name={name} placeholder={placeholder} id={name} />
    </div>
  )
}

export default Input
