import React, { useRef, useState, useEffect } from 'react';
import '../assets/variables.scss'
import axios from '../axios'
import Cookie from 'js-cookie'

function DragAndDropFile() {
    const [isDragging, setIsDragging] = useState(false);
    const fileInputRef = useRef(null);
    const access_token = Cookie.get('access_token');

    async function handleDragOver(e) {
        e.preventDefault();
        setIsDragging(true);
    }

    async function handleDragLeave(e) {
        e.preventDefault();
        setIsDragging(false);
    }

    async function handleDrop(e) {
        e.preventDefault();
        setIsDragging(false);
        const files = Array.from(e.dataTransfer.files);

        const formDataArray = files.map((file) => {
            const formData = new FormData();
            formData.append('file', file);
            return formData;
        });

        try {
            const responses = await Promise.all(formDataArray.map((formData) => {
                return axios.post('/upload_file', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'Authorization': `Bearer ${access_token}`
                    }
                });
            }));
            console.log(responses);
        } catch (error) {
            console.log(error.response.data.detail);
        }
    }


    async function handleFileInputChange(e) {
        const file = e.target.files[0];
        console.log(file);
    }

    useEffect(() => {
        async function handleWindowDragOver(event) {
            const dragOverElement = document.elementFromPoint(event.clientX, event.clientY);
            if (dragOverElement && dragOverElement.closest('.drag-and-drop')) {
                setIsDragging(true);
            } else {
                setIsDragging(false);
            }
        }

        window.addEventListener('dragover', handleWindowDragOver);

        return () => {
            window.removeEventListener('dragover', handleWindowDragOver);
        };
    }, []);

    return (
        <div className='drag-and-drop-block' onDragOver={handleDragOver} onDragLeave={handleDragLeave} onDrop={handleDrop}>
            <div className='drag-and-drop-file' style={{ display: isDragging ? 'flex' : 'none', opacity: isDragging ? 1 : 0 }}>
                <div className={`title`} style={{ opacity: 1 }}>Загрузить файлы</div>
            </div>
            <input type="file" style={{ display: 'none' }} ref={fileInputRef} onChange={handleFileInputChange} />
        </div>
    );
}

export default DragAndDropFile;
