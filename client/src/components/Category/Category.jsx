import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

import { useContextMenu } from '../../utils/contextMenu'
import {
  downloadFile,
  renameFile,
  addToBasketFile,
  addToFavoriteFile
} from '../../utils/fileActions';
import formatFileSize from '../../utils/formatFile'

import axios from '../../utils/axios';
import Cookie from 'js-cookie';

import '../../assets/variables.scss';
import styles from './Category.module.scss';

import DragAndDropFile from '../DragAndDropFile'
import SearchInput from '../SearchInput/SearchInput';
import Input from '../Input/Input';
import File from '../File/File';

function Category({ title, url }) {
  const { category_name } = useParams();

  const [files, setFiles] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const filteredFiles = files.filter((file) =>
    file.file_name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const [showRenameInput, setShowRenameInput] = useState(null);

  const access_token = Cookie.get('access_token');

  const {
    selectedItem,
    showContextMenuForItem,
    contextMenuPosition,
    handleContextMenuForItem,
    handleCloseContextMenu,
  } = useContextMenu();

  function handleSearch(query) {
    setSearchQuery(query);
  };

  function handleRenameInput(e) {
    e.preventDefault();
    setShowRenameInput(selectedItem.file_name.split('.')[0]);
  };

  useEffect(() => {
    async function getCategoryFiles() {
      try {
        let response;
        if (category_name) {
          response = await axios.get(`/files/${category_name}`, {
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          });
        } else {
          response = await axios.get(`${url}`, {
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          });
        }
        setFiles(response.data);
      } catch (error) {
        console.log(error.response.data.detail);
      }
    }
    getCategoryFiles();
  }, [category_name]);

  return (
    <div className="drag-and-drop">
      <DragAndDropFile 
         category_name={category_name}
      />
      <div className={styles.category} onClick={handleCloseContextMenu}>
        <div className={`title ${styles.categoryTitle}`}>
          {category_name !== undefined ? category_name : title}
        </div>
        <div className={styles.categoryContent}>

          {showContextMenuForItem && (
            <div className={styles.contextMenu} onClick={handleCloseContextMenu} style={{ left: contextMenuPosition.x, top: contextMenuPosition.y }}>
              <div className={styles.contextMenuItem} onClick={() => downloadFile(selectedItem, access_token)}>Скачать</div>
              <div className={styles.contextMenuItem} onClick={() => addToBasketFile(selectedItem, setFiles, files, access_token)}>Добавить избранное</div>
              <div className={styles.contextMenuItem} onClick={handleRenameInput}>Переименовать</div>
              <div className={styles.contextMenuItem} onClick={() => addToFavoriteFile(selectedItem, setFiles, files, access_token)}>В коризну</div>
            </div>
          )}

          <SearchInput title={"Поиск по файлам"} onSearch={handleSearch} />

          {showRenameInput != null && (
            <Input
              placeholder={"Имя"}
              value={showRenameInput}
              onChange={(e) => setShowRenameInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  renameFile(selectedItem, showRenameInput, setFiles, files, access_token);
                  setShowRenameInput(null)
                }
              }}
            />
          )}

          <div className={styles.files}>
            {filteredFiles.map((file) => {
              if (file.is_basket || file.is_favorite) {
                return null;
              }
              return (
                <File
                  key={file.file_id}
                  onContextMenu={(e) => handleContextMenuForItem(e, file)}
                  image={`../../img/categories/${file.file_content_type}.png`}
                  name={file.file_name.split('.')[0]}
                  extension={file.file_name.split('.')[1]}
                  size={formatFileSize(file.file_size)}
                />
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Category;