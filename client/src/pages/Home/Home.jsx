import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import Cookie from 'js-cookie'
import axios from '../../axios'

import styles from './Home.module.scss'
import '../../assets/variables.scss'

import Button from '../../components/Button/Button'
import SearchInput from '../../components/SearchInput/SearchInput'
import DragAndDropFile from '../../components/DragAndDropFile'

function Home() {
  const [history, setHistory] = useState([]);
  const access_token = Cookie.get('access_token');

  const [showFullFileName, setShowFullFileName] = useState([]);

  useEffect(() => {
    const initialState = history.map(() => false);
    setShowFullFileName(initialState);
  }, [history]);

  function handleNameClick(index) {
    setShowFullFileName(prevState => {
      const newState = [...prevState];
      newState[index] = !newState[index];
      return newState;
    });
  }

  useEffect(() => {
    async function getLastFiveFilesHistory() {
      try {
        const response = await axios.get(`/history/files/last_five`, {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });
        setHistory(response.data);
      } catch (error) {
        console.log(error.response.data.detail);
      }
    }
    getLastFiveFilesHistory();
  }, []);

  return (
    <div className="drag-and-drop">
      <DragAndDropFile />
      <div className={styles.home}>
        <form className={styles.search}>
          <SearchInput title={'Поиск по всем файлам'} />
          <Button title={'Найти'} marginTop={'37px'} />
        </form>

        <div className={styles.categories}>
          <div className={`title`}>Категории</div>
          <div className={styles.categoriesList}>
            <Link to="/category/folders" className={styles.categoriesElem}>
              <div className={styles.categoriesElemTitle}>
                <img src="img/categories/folder.png" alt="folder" />
                <p className={`dark-text`}>Папки</p>
              </div>
              <div className={styles.categoriesElemSpace}>
                <p className={`small-text`}>N файлов на N гб</p>
              </div>
            </Link>

            <Link to="/category/documents" className={styles.categoriesElem}>
              <div className={styles.categoriesElemTitle}>
                <img src="img/categories/documents.png" alt="documents" />
                <p className={`dark-text`}>Документы</p>
              </div>
              <div className={styles.categoriesElemSpace}>
                <p className={`small-text`}>N файлов на N гб</p>
              </div>
            </Link>

            <Link to="/category/images" className={styles.categoriesElem}>
              <div className={styles.categoriesElemTitle}>
                <img src="img/categories/images.png" alt="images" />
                <p className={`dark-text`}>Картинки</p>
              </div>
              <div className={styles.categoriesElemSpace}>
                <p className={`small-text`}>N файлов на N гб</p>
              </div>
            </Link>

            <Link to="/category/music" className={styles.categoriesElem}>
              <div className={styles.categoriesElemTitle}>
                <img src="img/categories/music.png" alt="music" />
                <p className={`dark-text`}>Музыка</p>
              </div>
              <div className={styles.categoriesElemSpace}>
                <p className={`small-text`}>N файлов на N гб</p>
              </div>
            </Link>

            <Link to="/category/videos" className={styles.categoriesElem}>
              <div className={styles.categoriesElemTitle}>
                <img src="img/categories/videos.png" alt="video" />
                <p className={`dark-text`}>Видео</p>
              </div>
              <div className={styles.categoriesElemSpace}>
                <p className={`small-text`}>N файлов на N гб</p>
              </div>
            </Link>
          </div>
        </div>

        <div className={styles.recent}>
          <div className={`title`}>Последние действия</div>
          <div className={styles.recentList}>
            <div className={styles.recentHeadlines}>
              <p className={`gray-text`}>Название</p>
              <p className={`gray-text`}>
                <img src="img/recent/action.png" alt="action" />
                Действие
              </p>
              <p className={`gray-text`}>
                <img src="img/recent/time.png" alt="time" />
                Последние изменения
              </p>
            </div>
            {history.map((history_elem, i) => (
              <div className={styles.recentElem} key={i + 1}>
                <div className={styles.recentElemTitle}>
                  <img src={`img/categories/${history_elem.file_contentType}.png`} alt="file" />

                  <p className={`dark-text`} onClick={() => handleNameClick(i)}>
                    {showFullFileName[i] ? history_elem.file_name : (
                      <>
                        {history_elem.file_name.slice(0, 5)}
                        <span className={`bold-text`}>...</span>
                        {history_elem.file_name.lastIndexOf('.') !== -1 && `.${history_elem.file_name.slice(history_elem.file_name.lastIndexOf('.') + 1)}`}
                      </>
                    )}
                  </p>

                </div>

                <div className={styles.recentElemAction}>
                  <p className={`dark-text`}>{history_elem.title}</p>
                </div>

                <div className={styles.recentElemDate}>
                  <p className={`dark-text`}>Дата: {history_elem.date}</p>
                  <p className={`dark-text`}>Время: {history_elem.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home
