import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import Cookie from 'js-cookie'
import axios from '../../axios'
import formatFileSize from '../../utils'

import styles from './Home.module.scss'
import '../../assets/variables.scss'

import Button from '../../components/Button/Button'
import SearchInput from '../../components/SearchInput/SearchInput'
import DragAndDropFile from '../../components/DragAndDropFile'

function Home() {
  const [categoryInfo, setCategoryInfo] = useState({
    documents: [0, 0],
    images: [0, 0],
    music: [0, 0],
    videos: [0, 0]
  });

  const [history, setHistory] = useState([]);
  const access_token = Cookie.get('access_token');

  const [showFullFileName, setShowFullFileName] = useState([]);

  useEffect(() => {
    async function getCategoryInfo() {
      try {

        const documentsResponse = await axios.get('/info/category/documents', {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });

        const imagesResponse = await axios.get('/info/category/images', {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });

        const musicResponse = await axios.get('/info/category/music', {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });

        const videosResponse = await axios.get('/info/category/videos', {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });

        setCategoryInfo({
          documents: [documentsResponse.data.total_count,
          formatFileSize(documentsResponse.data.total_size)],

          images: [imagesResponse.data.total_count,
          formatFileSize(imagesResponse.data.total_size)],

          music: [musicResponse.data.total_count,
          formatFileSize(musicResponse.data.total_size)],

          videos: [videosResponse.data.total_count,
          formatFileSize(videosResponse.data.total_size)],
        });
      } catch (error) {
        console.error(error.response.data);
      }
    };

    getCategoryInfo();
  }, []);

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
                <p className={`small-text`}>{categoryInfo["documents"][0]
                  + " файл(ов) на "} {categoryInfo["documents"][1]}
                </p>
              </div>
            </Link>

            <Link to="/category/images" className={styles.categoriesElem}>
              <div className={styles.categoriesElemTitle}>
                <img src="img/categories/images.png" alt="images" />
                <p className={`dark-text`}>Картинки</p>
              </div>
              <div className={styles.categoriesElemSpace}>
                <p className={`small-text`}>{categoryInfo["images"][0]
                  + " файл(ов) на "} {categoryInfo["images"][1]}
                </p>
              </div>
            </Link>

            <Link to="/category/music" className={styles.categoriesElem}>
              <div className={styles.categoriesElemTitle}>
                <img src="img/categories/music.png" alt="music" />
                <p className={`dark-text`}>Музыка</p>
              </div>
              <div className={styles.categoriesElemSpace}>
                <p className={`small-text`}>{categoryInfo["music"][0]
                  + " файл(ов) на "} {categoryInfo["music"][1]}
                </p>
              </div>
            </Link>

            <Link to="/category/videos" className={styles.categoriesElem}>
              <div className={styles.categoriesElemTitle}>
                <img src="img/categories/videos.png" alt="video" />
                <p className={`dark-text`}>Видео</p>
              </div>
              <div className={styles.categoriesElemSpace}>
                <p className={`small-text`}>{categoryInfo["videos"][0]
                  + " файл(ов) на "} {categoryInfo["videos"][1]}
                </p>              </div>
            </Link>
          </div>
        </div>

        <div className={styles.recent}>
          <div className={`title`}>Последние действия за сегодня</div>
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
