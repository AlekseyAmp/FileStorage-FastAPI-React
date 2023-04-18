import React, { useState, useEffect } from 'react';

import axios from '../../utils/axios';
import { useContextMenu } from '../../utils/contextMenu'
import {
    downloadFile,
    deleteFile,
    renameFile
} from '../../utils/fileActions';
import Cookie from 'js-cookie';

import '../../assets/variables.scss';

import File from '../File/File';
import Input from '../Input/Input'
import SearchInput from '../SearchInput/SearchInput';
import styles from './MovedFiles.module.scss';



function MovedFiles({ url, title, titleIcon, labelTitle, background, contextMenuBack, isFavorite }) {

    const categoryStyle = {
        background: background,
    };

    const [files, setFiles] = useState([]);

    const {
        handleContextMenu,
        handleCloseContextMenu,
        selectedFile,
        showContextMenu,
        contextMenuPosition,
    } = useContextMenu();

    const [showRenameInput, setShowRenameInput] = useState(false);

    const access_token = Cookie.get('access_token');

    async function handleRenameInput(e) {
        e.preventDefault();
        setShowRenameInput(selectedFile.name.split('.')[0]);
    }

    useEffect(() => {
        async function getMovedFiles() {
            try {
                const response = await axios.get(`/${url}`, {
                    headers: {
                        Authorization: `Bearer ${access_token}`,
                    },
                });
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

            {showRenameInput && (
                <Input
                    value={showRenameInput}
                    onChange={(e) => setShowRenameInput(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                            renameFile(selectedFile, showRenameInput);
                            setFiles(files.filter(file => file.file_id === selectedFile.file_id));
                        }
                    }}
                />
            )}

            {showContextMenu && (
                <div className={styles.contextMenu} onClick={handleCloseContextMenu} style={{ left: contextMenuPosition.x, top: contextMenuPosition.y }}>
                    <div className={styles.contextMenuItem} >{contextMenuBack}</div>
                    <div className={styles.contextMenuItem} onClick={() => downloadFile(selectedFile)}>Скачать</div>
                    <div className={styles.contextMenuItem} onClick={handleRenameInput}>Переименовать</div>
                    <div className={styles.contextMenuItem}>Поделиться</div>
                    {isFavorite ? null : <div className={styles.contextMenuItem} onClick={() => deleteFile(selectedFile, setFiles, files)}>Удалить</div>}
                </div>
            )}

            <SearchInput title={`Поиск по ${labelTitle}`} />

            <div className={styles.files}>
                {files.map((file) => (
                    <File
                        key={file.file_id}
                        onContextMenu={(e) => handleContextMenu(e, file)}
                        image={`../img/categories/${file.content_type}.png`}
                        name={file.name.split('.')[0]}
                        extension={file.name.split('.')[1]}
                        size={`${Math.floor(file.size / 1000)} КБ`}
                    />
                ))}
            </div>
        </div>
    )
}

export default MovedFiles