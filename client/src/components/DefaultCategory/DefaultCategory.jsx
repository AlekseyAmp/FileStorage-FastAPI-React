import React, { useState, useEffect } from 'react';

import { useContextMenu } from '../../utils/contextMenu'
import {
  downloadFile,
  renameFile,
  addToBasket,
  addToFavorite
} from '../../utils/fileActions';
import formatFileSize from '../../utils/formatFile'

import axios from '../../utils/axios';
import Cookie from 'js-cookie';

import '../../assets/variables.scss';
import styles from './DefaultCategory.module.scss';

import SearchInput from '../SearchInput/SearchInput';
import Input from '../Input/Input'
import File from '../File/File';

function DefaultCategory({ url, title, titleIcon, labelTitle, background }) {
  const defaultCategoryStyle = {
    background: background,
  };

  const [files, setFiles] = useState([]);

  const [fileImage, setFileImage] = useState()
  
  const [showRenameInput, setShowRenameInput] = useState(null);
 
  const access_token = Cookie.get('access_token');

  const {
    selectedItem,
    showContextMenuForItem,
    contextMenuPosition,
    handleContextMenuForItem,
    handleCloseContextMenu,
  } = useContextMenu();

  async function handleRenameInput(e) {
    e.preventDefault();
    setShowRenameInput(selectedItem.file_name.split('.')[0]);
  }

  // useEffect(() => {
  //   async function readFile() {
  //     try {
  //       const response = await axios.get(`files/read/${selectedFile.file_id}`, {
  //         headers: {
  //           'Authorization': `Bearer ${access_token}`
  //         }
  //       });
  //       setFileImage(response.data)
  //       console.log(response.data)
  //     } catch (error) {
  //       console.log(error.response.data.detail);
  //     }
  //   }
  //   readFile();
  // }, []);

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

  return (
    <div className={styles.defaultCategory} style={defaultCategoryStyle} onClick={handleCloseContextMenu}>
      <div className={`title ${styles.defaultCategoryTitle}`}>
        {titleIcon}
        {title}
      </div>
      <div className={styles.defaultCategoryContent}>

        {showRenameInput != null && (
          <Input
            placeholder={"Имя"}
            value={showRenameInput}
            onChange={(e) => setShowRenameInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                renameFile(selectedItem, showRenameInput);
                setShowRenameInput(null)
              }
            }}
          />
        )}

        {showContextMenuForItem && (
          <div className={styles.contextMenu} onClick={handleCloseContextMenu} style={{ left: contextMenuPosition.x, top: contextMenuPosition.y }}>
            <div className={styles.contextMenuItem} onClick={() => downloadFile(selectedItem)}>Скачать</div>
            <div className={styles.contextMenuItem} onClick={() => addToFavorite(selectedItem, setFiles, files)}>Добавить избранное</div>
            <div className={styles.contextMenuItem} onClick={handleRenameInput}>Переименовать</div>
            <div className={styles.contextMenuItem} onClick={() => addToBasket(selectedItem, setFiles, files)}>В коризну</div>
          </div>
        )}

        <SearchInput title={`Поиск по ${labelTitle}`} />

        <div className={styles.files}>
          {files.map((file) => {
            if (file.is_basket || file.is_favorite) {
              return null;
            }
            return (
              <File
                key={file.file_id}
                onContextMenu={(e) => handleContextMenuForItem(e, file)}
                image={fileImage}
                name={file.file_name.split('.')[0]}
                extension={file.file_name.split('.')[1]}
                size={formatFileSize(file.file_size)}
              />
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default DefaultCategory;