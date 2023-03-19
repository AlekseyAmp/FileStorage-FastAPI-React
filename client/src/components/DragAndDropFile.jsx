import React, { useRef, useState, useEffect } from 'react';
import '../assets/variables.scss'
import axios from '../axios'


function DragAndDropFile() {
    const [isDragging, setIsDragging] = useState(false);
    const fileInputRef = useRef(null);

    function handleDragOver(event) {
        event.preventDefault();
        setIsDragging(true);
    }

    function handleDragLeave(event) {
        event.preventDefault();
        setIsDragging(false);
    }

    function handleDrop(event) {
        event.preventDefault();
        setIsDragging(false);
        const file = event.dataTransfer.files[0];
        console.log(file);

        const formData = new FormData();
        formData.append('file', file);

        axios.post('/uploadfile', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }).then(response => {
            console.log(response);
        }).catch(error => {
            console.log(error);
        });
    }

    function handleFileInputChange(event) {
        const file = event.target.files[0];
        console.log(file);
        // Do something with the file, e.g. upload it to the server
    }

    useEffect(() => {
        function handleWindowDragOver(event) {
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
