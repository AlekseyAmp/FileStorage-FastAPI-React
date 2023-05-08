import React, { useEffect, useState } from 'react';

import Cookie from 'js-cookie';
import axios from '../../utils/axios';

import styles from './History.module.scss';
import '../../assets/variables.scss';

import SearchInput from '../../components/SearchInput/SearchInput';

function History() {
  const [history, setHistory] = useState({});
  const access_token = Cookie.get('access_token');

  const [searchQuery, setSearchQuery] = useState('');

  async function getFilesHistory() {
    try {
      const response = await axios.get(`/history`, {
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      });
      setHistory(response.data);
    } catch (error) {
      console.log(error.response.data.detail);
    }
  }

  useEffect(() => {
    getFilesHistory();
  }, []);

  const filteredHistory = {};
  Object.entries(history).forEach(([date, historyElems]) => {
    const filteredElems = historyElems.filter((elem) =>
      elem.description.toLowerCase().includes(searchQuery.toLowerCase())
    );
    if (filteredElems.length > 0) {
      filteredHistory[date] = filteredElems;
    }
  });

  function handleSearch(query) {
    setSearchQuery(query);
  }

  return (
    <div className={styles.history}>
      <div className={'title'}>История</div>
      <SearchInput onSearch={handleSearch} />
      <div className={styles.historyContent}>
        {Object.entries(filteredHistory).map(([date, historyElems]) => (
          <div className={styles.historyElem} key={date}>
            <h3 className={'bold-text'}>Дата: {date}</h3>

            {historyElems.map((historyElem, i) => (
              <div className={styles.historyElemContent} key={i + 1}>
                <p className={'dark-text'}>
                  {historyElem.time}
                  <span className={`dark-text ${styles.historyElemDescription}`}>
                    {historyElem.description}
                  </span>
                </p>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

export default History;
