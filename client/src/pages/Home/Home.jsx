import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import Cookie from 'js-cookie'
import axios from '../../utils/axios'
import formatFileSize from '../../utils/formatFile'

import styles from './Home.module.scss'
import '../../assets/variables.scss'

import Button from '../../components/Button/Button'
import SearchInput from '../../components/SearchInput/SearchInput'
import DragAndDropFile from '../../components/DragAndDropFile'

function Home() {
  const [categoriesInfo, setCategoriesInfo] = useState({
    customCategories: [0, 0],
    documents: [0, 0],
    images: [0, 0],
    music: [0, 0],
    videos: [0, 0]
  });

  const [history, setHistory] = useState([]);
  const access_token = Cookie.get('access_token');

  const [showFullName, setShowFullName] = useState([]);

  useEffect(() => {
    async function getCategoriesInfo() {
      try {

        const customCategoriesResponse = await axios.get('/categories/info', {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });

        const documentsResponse = await axios.get('/files/info/documents', {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });

        const imagesResponse = await axios.get('/files/info/images', {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });

        const musicResponse = await axios.get('/files/info/music', {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });

        const videosResponse = await axios.get('/files/info/videos', {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });

        setCategoriesInfo({
          customCategories: [customCategoriesResponse.data.total_count,
          formatFileSize(customCategoriesResponse.data.total_size)],

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

    getCategoriesInfo();
  }, []);

  useEffect(() => {
    async function getLastFiveHistory() {
      try {
        const response = await axios.get(`/history/recent`, {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });
        setHistory(response.data);
      } catch (error) {
        console.log(error.response.data.detail);
      }
    }
    getLastFiveHistory();
  }, []);

  useEffect(() => {
    const initialState = history.map(() => false);
    setShowFullName(initialState);
  }, [history]);

  function handleNameClick(index) {
    setShowFullName(prevState => {
      const newState = [...prevState];
      newState[index] = !newState[index];
      return newState;
    });
  }

  return (
    <div className="drag-and-drop">
      <DragAndDropFile />
      <div className={styles.home}>
        <SearchInput title={'Поиск по всем файлам'} />

        <div className={styles.categories}>
          <div className={`title`}>Категории</div>
          <div className={styles.categoriesList}>
            <Link to="/categories/custom" className={styles.categoriesElem}>
              <div className={styles.categoriesElemTitle}>
                <img src="img/categories/folder.png" alt="folder" />
                <p className={`dark-text`}>Мои категории</p>
              </div>
              <div className={styles.categoriesElemSpace}>
                <p className={`small-text`}>{categoriesInfo["customCategories"][0]
                  + " категори(и/й) на "} {categoriesInfo["customCategories"][1]}
                </p>
              </div>
            </Link>

            <Link to="/categories/default/documents" className={styles.categoriesElem}>
              <div className={styles.categoriesElemTitle}>
                <img src="img/categories/documents.png" alt="documents" />
                <p className={`dark-text`}>Документы</p>
              </div>
              <div className={styles.categoriesElemSpace}>
                <p className={`small-text`}>{categoriesInfo["documents"][0]
                  + " файл(ов) на "} {categoriesInfo["documents"][1]}
                </p>
              </div>
            </Link>

            <Link to="/categories/default/images" className={styles.categoriesElem}>
              <div className={styles.categoriesElemTitle}>
                <img src="img/categories/images.png" alt="images" />
                <p className={`dark-text`}>Картинки</p>
              </div>
              <div className={styles.categoriesElemSpace}>
                <p className={`small-text`}>{categoriesInfo["images"][0]
                  + " файл(ов) на "} {categoriesInfo["images"][1]}
                </p>
              </div>
            </Link>

            <Link to="/categories/default/music" className={styles.categoriesElem}>
              <div className={styles.categoriesElemTitle}>
                <img src="img/categories/music.png" alt="music" />
                <p className={`dark-text`}>Музыка</p>
              </div>
              <div className={styles.categoriesElemSpace}>
                <p className={`small-text`}>{categoriesInfo["music"][0]
                  + " файл(ов) на "} {categoriesInfo["music"][1]}
                </p>
              </div>
            </Link>

            <Link to="/categories/default/videos" className={styles.categoriesElem}>
              <div className={styles.categoriesElemTitle}>
                <img src="img/categories/videos.png" alt="video" />
                <p className={`dark-text`}>Видео</p>
              </div>
              <div className={styles.categoriesElemSpace}>
                <p className={`small-text`}>{categoriesInfo["videos"][0]
                  + " файл(ов) на "} {categoriesInfo["videos"][1]}
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
            {history.map((history_elem, i) => {
              const name = history_elem.name;
              return (
                <div className={styles.recentElem} key={i + 1}>
                  <div className={styles.recentElemTitle}>
                    <p className={`dark-text`} onClick={() => handleNameClick(i)}>
                    {showFullName[i] ? (
                        <>
                          {name}
                        </>
                      ) : (
                        <>
                          {name.length > 10 ? (
                            <>
                              {name.substring(0, 10)}
                              <span className={`bold-text`}>...</span>
                            </>
                          ) : (
                            name
                          )}
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
              );
            })}

          </div>
        </div>
      </div>
    </div>
  )
}

export default Home;
