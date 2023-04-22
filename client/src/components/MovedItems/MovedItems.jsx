import React, { useState, useEffect } from 'react';

import axios from '../../utils/axios';
import { useContextMenu } from '../../utils/contextMenu'
import {
    downloadFile,
    deleteFile,
    renameFile,
    revertMovedFile
} from '../../utils/fileActions';
import formatFileSize from '../../utils/formatFile'

import Cookie from 'js-cookie';

import '../../assets/variables.scss';

import File from '../File/File';
import Input from '../Input/Input'
import SearchInput from '../SearchInput/SearchInput';
import styles from './MovedItems.module.scss';

function MovedItems({ url, title, titleIcon, labelTitle, background, contextMenuBack, isFavorite }) {

    const categoryStyle = {
        background: background,
    };

    const [files, setFiles] = useState([]);

    const [showRenameInput, setShowRenameInput] = useState(null);
    
    const access_token = Cookie.get('access_token');

    const {
        selectedItem,
        showContextMenuForItem,
        contextMenuPosition,
        handleContextMenuForItem,
        handleCloseContextMenu,
      } = useContextMenu();

    function handleRenameInput(e) {
        e.preventDefault();
        setShowRenameInput(selectedItem.file_name.split('.')[0]);
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

            {showContextMenuForItem && (
                <div className={styles.contextMenu} onClick={handleCloseContextMenu} style={{ left: contextMenuPosition.x, top: contextMenuPosition.y }}>
                    <div className={styles.contextMenuItem} onClick={() => revertMovedFile(selectedItem, setFiles, files)}>{contextMenuBack}</div>
                    <div className={styles.contextMenuItem} onClick={() => downloadFile(selectedItem)}>Скачать</div>
                    <div className={styles.contextMenuItem} onClick={handleRenameInput}>Переименовать</div>
                    {isFavorite ? null : <div className={styles.contextMenuItem} onClick={() => deleteFile(selectedItem, setFiles, files)}>Удалить</div>}
                </div>
            )}
            <SearchInput title={`Поиск по ${labelTitle}`} />

            {showRenameInput != null && (
                <Input
                    value={showRenameInput}
                    onChange={(e) => setShowRenameInput(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                            renameFile(selectedItem, showRenameInput);
                            setShowRenameInput(null)
                        }
                    }}
                />
            )}
            
            <div className={styles.files}>
                {files.map((file) => (
                    <File
                        key={file.file_id}
                        onContextMenu={(e) => handleContextMenuForItem(e, file)}
                        image={`../img/categories/${file.content_type}.png`}
                        name={file.file_name.split('.')[0]}
                        extension={file.file_name.split('.')[1]}
                        size={formatFileSize(file.file_size)}
                    />
                ))}
            </div>
        </div>
    )
}

export default MovedItems;