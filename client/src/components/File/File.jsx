import { React, useState } from 'react';
import '../../assets/variables.scss';
import styles from './File.module.scss'


function File({name, size, image, onContextMenu }) {
  const [showSelectedFile, setShowSelectedFile] = useState(false);


  
  return (
    <div className={styles.file}
     onContextMenu={onContextMenu}>
      <img src={image} alt="images" />
      <div className={styles.fileText}>
        <p className={`dark-text`}>{name}</p>
        <p className={`small-text`}>Вес: {size}</p>
      </div>
    </div>
  );
}

export default File