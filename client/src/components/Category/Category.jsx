import React, { useState } from 'react';

import '../../assets/variables.scss';

import SearchInput from '../../components/SearchInput/SearchInput'
import styles from './Category.module.scss'

function Category({ title, titleIcon, labelTitle, background  }) {
  const categoryStyle = {
    background: background
  };

  const [showContextMenu, setShowContextMenu] = useState(false);

  const handleContextMenu = (event) => {
    event.preventDefault();
    setShowContextMenu(true);
  };

  const handleCloseContextMenu = () => {
    setShowContextMenu(false);
  };

  return (
    <div className={styles.category} style={categoryStyle} onClick={handleCloseContextMenu}>
      <div className={`title ${styles.categoryTitle}`}>
        {titleIcon}
        {title}
      </div>
      <div className={styles.categoryContent}>
        <SearchInput title={`Поиск по ${labelTitle}`}/>

        <div className={styles.files}>
          <div className={styles.filesElem} onContextMenu={handleContextMenu}>
            <img src="../img/example.png" alt="images" />
            <div className={styles.filesElemText}>
              <p className={`dark-text`}>Пример</p>
              <p className={`small-text`}>Вес: N гб</p>
            </div>
          </div>
        </div>

        {showContextMenu && (
          <div className={styles.contextMenu} onClick={handleCloseContextMenu}>
            <div className={styles.contextMenuItem}>Открыть</div>
            <div className={styles.contextMenuItem}>Переименовать</div>
            <div className={styles.contextMenuItem}>Поделиться</div>
            <div className={styles.contextMenuItem}>Добавить в избранное</div>
            <div className={styles.contextMenuItem}>Удалить</div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Category;
