import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import { useContextMenu } from '../../../utils/contextMenu'
import {
  createCategory,
  deleteCategory,
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
  const [searchQuery, setSearchQuery] = useState('');
  const filterCategories = categories.filter((category) =>
    category.category_name.toLowerCase().includes(searchQuery.toLowerCase())
  );

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

  function handleSearch(query) {
    setSearchQuery(query);
  };

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
        <SearchInput title="Поиск по категориям" onSearch={handleSearch} />
        <Button onClick={handleNewCategoryInput} title={`Создать категорию`} marginTop={`40px`} />
      </div>

      {showNewCategoryInput != null && (
        <Input
          placeholder={'Придумайте название'}
          value={showNewCategoryInput}
          onChange={(e) => setShowNewCategoryInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              createCategory(showNewCategoryInput, setCategories, categories)
              setShowNewCategoryInput(null)
            }
          }}
        />
      )}

      <div className={styles.customCategoryContent}>

        {showContextMenuForItem && (
          <div className={styles.contextMenu} onClick={handleCloseContextMenu} style={{ left: contextMenuPosition.x, top: contextMenuPosition.y }}>
            <div className={styles.contextMenuItem}>Скачать</div>
            <div className={styles.contextMenuItem} onClick={handleRenameInput}>Переименовать</div>
            <div className={styles.contextMenuItem} onClick={() => deleteCategory(selectedItem, setCategories, categories)}>Удалить</div>
          </div>
        )}

        {showRenameInput !== null && (
          <Input
            value={showRenameInput}
            onChange={(e) => setShowRenameInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                renameCategory(selectedItem, showRenameInput, setCategories, categories);
                setShowRenameInput(null)
              }
            }}
          />
        )}

        <div className={styles.customCategories}>
          {filterCategories.map((category) => {
            return (
              <CustomCategory
                key={category.category_id}
                onContextMenu={(e) => handleContextMenuForItem(e, category)}
                onDoubleClick={() => navigate(`/categories/custom/${category.category_name}`)}
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
