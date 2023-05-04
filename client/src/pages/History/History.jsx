import React, { useEffect, useState } from 'react';

import Cookie from 'js-cookie';
import axios from '../../utils/axios';

import styles from './History.module.scss';
import '../../assets/variables.scss';

import SearchInput from '../../components/SearchInput/SearchInput';

function History() {
  const [history, setHistory] = useState({});
  const access_token = Cookie.get('access_token');
  
  useEffect(() => {
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
    getFilesHistory();
  }, []);

  return (
    <div className={styles.history} >
      <div className={'title'}>История</div>
      <SearchInput />
      <div className={styles.historyContent}>
        {Object.entries(history).map(([date, history_elems]) => (

          <div className={styles.historyElem} key={date}>
            <h3 className={'bold-text'}>Дата: {date}</h3>

            {history_elems.map((history_elem, i) => (
              <div className={styles.historyElemContent} key={i + 1}>
                <p className={'dark-text'}>
                  {history_elem.time}
                  <span className={`dark-text ${styles.historyElemDescription}`}>{history_elem.description}</span>
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