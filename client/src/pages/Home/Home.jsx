import React from 'react'
import { Link } from 'react-router-dom'

import styles from './Home.module.scss'
import '../../assets/variables.scss'

import Button from '../../components/Button/Button'
import SearchInput from '../../components/SearchInput/SearchInput'

function Home() {
  return (
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
              <img src="img/categories/docs.png" alt="documents" />
              <p className={`dark-text`}>Документы</p>
            </div>
            <div className={styles.categoriesElemSpace}>
              <p className={`small-text`}>N файлов на N гб</p>
            </div>
          </Link>

          <Link to="/category/images" className={styles.categoriesElem}>
            <div className={styles.categoriesElemTitle}>
              <img src="img/categories/image.png" alt="images" />
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
        <div className={`title`}>Последние файлы</div>
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
          <div className={styles.recentElem}>
            <div className={styles.recentElemTitle}>
              <img src="img/recent/clock-folder.png" alt="folder" />
              <p className={`dark-text`}>Круто...</p>
            </div>

            <div className={styles.recentElemAction}>
              <p className={`dark-text`}>Перемещение в корзину</p>
            </div>

            <div className={styles.recentElemDate}>
              <p className={`dark-text`}>1 мая 2023 г.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home
