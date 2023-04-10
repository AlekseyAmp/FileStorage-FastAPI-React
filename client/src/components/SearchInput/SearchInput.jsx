import React, { useState } from 'react'

import styles from './SearchInput.module.scss'

function SearchInput({ title }) {
  return (
    <div className={styles.inputForm}>
      <label htmlFor="search" className={`dark-text`}>{title}</label>
      <input type="text" placeholder='Поиск' onChange={handleInputChange} />
    </div>
  )
}

export default SearchInput
