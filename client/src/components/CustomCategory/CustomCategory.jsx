import React, { useState } from 'react';
import '../../assets/variables.scss';
import styles from './CustomCategory.module.scss';

function CustomCategory({ name, size, image, onContextMenu, onDoubleClick }) {
  const [showFullCategoryName, setShowFullCategoryName] = useState(false);

  function handleNameClick() {
    setShowFullCategoryName(!showFullCategoryName);
  }

  return (
    <div className={styles.customCategory} onDoubleClick={onDoubleClick} onContextMenu={onContextMenu}>
      <img src={image} alt="customCategory" />
      <div className={styles.customCategoryText}>
        <p className={`dark-text`} onClick={handleNameClick}>
          {showFullCategoryName ? (
            `${name}`
          ) : (
            <>
              {name.length > 10 ? (
                <>
                  {name.substring(0, 10)}
                  <span className={`bold-text`}>...</span>
                </>
              ) : (
                name
              )}
            </>
          )}

        </p>
        <p className={`small-text`}>Вес: {size}</p>
      </div>
    </div>
  );
}

export default CustomCategory;
