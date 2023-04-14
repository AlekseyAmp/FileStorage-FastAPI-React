import React, { useState } from 'react';
import '../../assets/variables.scss';
import styles from './File.module.scss';

function File({ name, size, image, onContextMenu }) {
  const [showFullFileName, setShowFullFileName] = useState(false);

  const fileExtension = name.slice(name.lastIndexOf('.') + 1);
 
  function handleNameClick() {
    setShowFullFileName(!showFullFileName);
  }

  return (
    <div className={styles.file} onContextMenu={onContextMenu}>
      <img src={image} alt="file" />
      <div className={styles.fileText}>
        <p className={`dark-text`} onClick={handleNameClick}>
          {showFullFileName ? name : (
            <>
              {name.slice(0, 5)}
              <span className={`bold-text`}>...</span>
              {fileExtension && `.${fileExtension}`}
            </>
          )}
        </p>
        <p className={`small-text`}>Вес: {size}</p>
      </div>
    </div>
  );
}

export default File;
