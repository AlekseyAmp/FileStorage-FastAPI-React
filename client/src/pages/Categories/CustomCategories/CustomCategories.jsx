import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import { useContextMenu } from '../../../utils/contextMenu'
import {
  createCategory,
  renameCategory,
} from '../../../utils/categoryActions';
import formatFileSize from '../../../utils/formatFile'

import axios from '../../../utils/axios';
import Cookie from 'js-cookie'

import '../../../assets/variables.scss';
import styles from './CustomCategories.module.scss';

import CustomCategory from '../../../components/CustomCategory/CustomCategory'
import Input from '../../../components/Input/Input'
import SearchInput from '../../../components/SearchInput/SearchInput'
import Button from '../../../components/Button/Button'

function CustomCategories() {
  const [categories, setCategories] = useState([]);
  const navigate = useNavigate();

  const [showRenameInput, setShowRenameInput] = useState(null);
  const [showNewCategoryInput, setShowNewCategoryInput] = useState(null);

  const access_token = Cookie.get('access_token');

  const {
    showContextMenuForItem,
    selectedItem,
    contextMenuPosition,
    handleContextMenuForItem,
    handleCloseContextMenu,
  } = useContextMenu();

  function handleNewCategoryInput(e) {
    e.preventDefault();
    setShowNewCategoryInput('');
  }

  function handleRenameInput(e) {
    e.preventDefault();
    setShowRenameInput(selectedItem.category_name);
  }

  useEffect(() => {
    async function getCategoryFiles() {
      try {
        const response = await axios.get(`/categories`, {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });
        setCategories(response.data);
      } catch (error) {
        console.log(error.response.data.detail);
      }
    }
    getCategoryFiles();
  }, []);

  return (
    <div className={styles.customCategory} onClick={(e) => { handleCloseContextMenu(); }}>
      <div className={`title ${styles.categoryTitle}`}>
        Собственные категории
      </div>

      <div className={styles.customCategoryHelp}>
        <SearchInput title={`Поиск по своим категориям`} />
        <Button onClick={handleNewCategoryInput} title={`Создать категорию`} marginTop={`40px`} />
      </div>

      {showNewCategoryInput != null && (
        <Input
          placeholder={'Придумайте название'}
          value={showNewCategoryInput}
          onChange={(e) => setShowNewCategoryInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              createCategory(showNewCategoryInput);
            }
          }}
        />
      )}

      <div className={styles.customCategoryContent}>

        {showContextMenuForItem && (
          <div className={styles.contextMenu} onClick={handleCloseContextMenu} style={{ left: contextMenuPosition.x, top: contextMenuPosition.y }}>
            <div className={styles.contextMenuItem}>Скачать</div>
            <div className={styles.contextMenuItem}>Добавить избранное</div>
            <div className={styles.contextMenuItem} onClick={handleRenameInput}>Переименовать</div>
            <div className={styles.contextMenuItem}>В коризну</div>
          </div>
        )}

        {showRenameInput !== null && (
          <Input
            value={showRenameInput}
            onChange={(e) => setShowRenameInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                renameCategory(selectedItem.category_name, showRenameInput);
              }
            }}
          />
        )}

        <div className={styles.customCategories}>
          {categories.map((category) => {
            if (category.is_basket || category.is_favorite) {
              return null;
            }
            return (
              <CustomCategory
                key={category.category_id}
                onContextMenu={(e) => handleContextMenuForItem(e, category)}
                onDoubleClick={() => navigate(`/category/custom/${category.category_name}`)}
                image={`../img/categories/folder.png`}
                name={category.category_name}
                size={formatFileSize(category.category_size)}
              />
            );
          })}
        </div>
      </div>
    </div>
  )
}

export default CustomCategories;
