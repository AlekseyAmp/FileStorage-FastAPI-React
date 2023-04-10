import React, { useState, useEffect } from 'react';

import axios from '../../axios';
import Cookie from 'js-cookie';

import '../../assets/variables.scss';
import styles from './Category.module.scss';

import SearchInput from '../SearchInput/SearchInput';
import Input from '../Input/Input'
import File from '../File/File';

function Category({ url, title, titleIcon, labelTitle, background }) {
  const categoryStyle = {
    background: background,
  };

  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);

  const [showContextMenu, setShowContextMenu] = useState(false);

  const [contextMenuPosition, setContextMenuPosition] = useState({ x: 0, y: 0 });
  const [showRenameInput, setShowRenameInput] = useState(false);

  const access_token = Cookie.get('access_token');


  useEffect(() => {
    async function getCategoryFiles() {
      try {
        const response = await axios.get(`${url}`, {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });
        setFiles(response.data);
      } catch (error) {
        console.log(error.response.data.detail);
      }
    }
    getCategoryFiles();
  }, []);

  async function handleContextMenu(e, file) {
    e.preventDefault();
    setSelectedFile(file);
    setShowContextMenu(true);
    setContextMenuPosition({ x: e.pageX, y: e.pageY });
  }

  async function handleCloseContextMenu(e) {
    e.preventDefault();
    setShowContextMenu(false);
  }

  async function handleDownload() {
    try {
      const response = await axios.get(`files/download/${selectedFile.file_id}`, {
        headers: {
          'Authorization': `Bearer ${access_token}`
        }
      });
      const url = window.URL.createObjectURL(new Blob([response.data], { type: selectedFile.content_type }));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', selectedFile.name);
      document.body.appendChild(link);
      link.click();
    } catch (error) {
      console.log(error.response.data.detail);
    }
  }
  
  async function handleRename(newName) {
    try {
      const response = await axios.patch(`files/rename/${selectedFile.file_id}/${newName}`, newName, {
        headers: {
          'Authorization': `Bearer ${access_token}`
        }
      });
    } catch (error) {
      console.log(error.response.data.detail);
    }
  }

  async function handleRenameInput(e) {
    e.preventDefault();
    setShowRenameInput((selectedFile.name).split('.')[0]);
  }

  async function handleInBasket() {
    try {
      const response = await axios.patch(`files/in_basket/${selectedFile.file_id}`, {}, {
        headers: {
          'Authorization': `Bearer ${access_token}`
        }
      });
      console.log(response.data);
      setFiles(files.filter(file => file.file_id !== selectedFile.file_id));
    } catch (error) {
      console.log(error.response.data.detail);
    }
  }

  async function handleInFavorite() {
    try {
      const response = await axios.patch(`files/in_favorite/${selectedFile.file_id}`, {}, {
        headers: {
          'Authorization': `Bearer ${access_token}`
        }
      });
      console.log(response.data)
    } catch (error) {
      console.log(error.response.data.detail);
    }
  }

  return (
    <div className={styles.category} style={categoryStyle} onClick={handleCloseContextMenu}>
      <div className={`title ${styles.categoryTitle}`}>
        {titleIcon}
        {title}
      </div>
      <div className={styles.categoryContent}>

        {showRenameInput && (
          <Input
            value={showRenameInput}
            onChange={(e) => setShowRenameInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                handleRename(showRenameInput);
                setFiles(files.filter(file => file.file_id === selectedFile.file_id));
              }
            }}
          />
        )}

        {showContextMenu && (
          <div className={styles.contextMenu} onClick={handleCloseContextMenu} style={{ left: contextMenuPosition.x, top: contextMenuPosition.y }}>
            <div className={styles.contextMenuItem} onClick={handleDownload}>Скачать</div>
            <div className={styles.contextMenuItem} onClick={handleInFavorite}>Добавить избранное</div>
            <div className={styles.contextMenuItem} onClick={handleRenameInput}>Переименовать</div>
            <div className={styles.contextMenuItem}>Поделиться</div>
            <div className={styles.contextMenuItem} onClick={handleInBasket}>В коризну</div>
          </div>
        )}

        <SearchInput title={`Поиск по ${labelTitle}`} />
            
        <div className={styles.files}>    
          {files.map((file) => {
            if (file.is_deleted) {
              return null;
            }
            return (
              <File
                key={file.file_id}
                onContextMenu={(e) => handleContextMenu(e, file)}
                image={`../img/categories/${file.content_type}.png`}
                name={file.name}
                size={`${Math.floor(file.size / 1000)} КБ`}
              />
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default Category;