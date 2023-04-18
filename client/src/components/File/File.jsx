import React, { useState } from 'react';
import '../../assets/variables.scss';
import styles from './File.module.scss';

function File({ name, extension, size, image, onContextMenu }) {
  const [showFullFileName, setShowFullFileName] = useState(false);

  function handleNameClick() {
    setShowFullFileName(!showFullFileName);
  }

  return (
    <div className={styles.file} onContextMenu={onContextMenu}>
      <img src={image} alt="file" />
      <div className={styles.fileText}>
        <p className={`dark-text`} onClick={handleNameClick}>
          {showFullFileName ? (
            `${name}.${extension}`
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
              {extension && `.${extension}`}
            </>
          )}

        </p>
        <p className={`small-text`}>Вес: {size}</p>
      </div>
    </div>
  );
}

export default File;

