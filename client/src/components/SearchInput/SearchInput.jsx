import React from 'react';

import styles from './SearchInput.module.scss';

function SearchInput({ title, onSearch }) {
  function handleChange(e) {
    onSearch(e.target.value);
  };

  return (
    <div className={styles.inputForm}>
      <label htmlFor="search" className={`dark-text`}>
        {title}
      </label>
      <input type="text" placeholder="Поиск" onChange={handleChange} />
    </div>
  );
}

export default SearchInput;
