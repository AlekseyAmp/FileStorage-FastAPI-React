import { React } from 'react';
import '../../assets/variables.scss';
import styles from './File.module.scss'


function File(props) {
    const {filename, fileformat, size, image } = props;
    return (
      <div className={styles.file} onContextMenu={props.onContextMenu}>
        <img src={image} alt="images" />
        <div className={styles.fileText}>
          <p className={`dark-text`}>{filename}.{fileformat}</p>
          <p className={`small-text`}>Вес: {size}</p>
        </div>
      </div>
    );
}

export default File
