import React, { useState, useEffect } from 'react';
import axios from '../../axios';
import Cookie from 'js-cookie';

import '../../assets/variables.scss';

import File from '../File/File';
import SearchInput from '../SearchInput/SearchInput';
import styles from './MovedFiles.module.scss';


function MovedFiles({ url, title, titleIcon, labelTitle, background }) {

    const categoryStyle = {
        background: background,
    };

    const [files, setFiles] = useState([]);

    const access_token = Cookie.get('access_token')

    useEffect(() => {
        async function getMovedFiles() {
            try {
                const response = await axios.get(`/${url}`, {
                    headers: {
                        Authorization: `Bearer ${access_token}`,
                    },
                });
                console.log(response.data)
                setFiles(response.data);
            } catch (error) {
                console.log(error.response.data.detail);
            }
        }
        getMovedFiles();
    }, []);

    return (
        <div className={styles.movedFiles} style={categoryStyle}>

            <div className={`title ${styles.movedFilesTitle}`}>
                {titleIcon}
                {title}
            </div>

            <SearchInput title={`Поиск по ${labelTitle}`} />

            <div className={styles.files}>
                {files.map((file) => (
                    <File
                        key={file.file_id}
                        image={`../img/categories/${file.content_type}.png`}
                        name={file.name}
                        size={`${Math.floor(file.size / 1000)} КБ`}
                    />
                ))}
            </div>
        </div>
    )
}

export default MovedFiles