import React, { useState, useEffect } from 'react';
import axios from '../../axios'
import Cookie from 'js-cookie';

import '../../assets/variables.scss';

import File from '../File/File';
import SearchInput from '../SearchInput/SearchInput'
import styles from './Category.module.scss'

function Category(props) {

  const { categoryName, imagePath, title, titleIcon, labelTitle, background } = props;

  const categoryStyle = {
    background: background
  };

  const [files, setFiles] = useState([]);
  const [showContextMenu, setShowContextMenu] = useState(false);
  const access_token = Cookie.get('access_token');
  const [contextMenuPosition, setContextMenuPosition] = useState({ x: 0, y: 0 });


  useEffect(() => {
    async function getCategoryFiles() {
      try {
        const response = await axios.get(`/category/${categoryName}`, {
          headers: {
            'Authorization': `Bearer ${access_token}`
          }
        });
        setFiles(response.data.files);
      } catch (error) {
        console.error(error);
      }
    };
    getCategoryFiles();
  }, []);



    async function handleContextMenu(e) {
      e.preventDefault();
      setShowContextMenu(true);
      setContextMenuPosition({ x: e.pageX, y: e.pageY });
    };


    async function handleCloseContextMenu(e) {
      setShowContextMenu(false);
    };

  return (
    <div className={styles.category} style={categoryStyle} onClick={handleCloseContextMenu}>
      <div className={`title ${styles.categoryTitle}`}>
        {titleIcon}
        {title}
      </div>
      <div className={styles.categoryContent}>
        <SearchInput title={`Поиск по ${labelTitle}`} />

        <div className={styles.files}>

          {files.map((file) => (
            <File
              key={file.file_id}
              onContextMenu={handleContextMenu}
              image={`../img/categories/${imagePath}`}
              filename={file.filename}
              fileformat={file.fileformat}
              size={Math.floor(file.size / 1000) + ' КБ'}
            />
          ))}

        </div>

        {showContextMenu && (
          <div className={styles.contextMenu} onClick={handleCloseContextMenu} style={{ left: contextMenuPosition.x, top: contextMenuPosition.y }}>
            <div className={styles.contextMenuItem}>Скачать</div>
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
