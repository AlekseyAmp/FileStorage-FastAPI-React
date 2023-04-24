import axios from '../utils/axios';
import Cookie from 'js-cookie';

const access_token = Cookie.get('access_token');

async function downloadFile(selectedFile) {
  try {
    const response = await axios.get(`files/download/${selectedFile.file_id}`, {
      headers: {
        'Authorization': `Bearer ${access_token}`
      },
      responseType: 'blob'
    });
    const blob = new Blob([response.data], { type: selectedFile.file_content_type });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', selectedFile.file_name);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.log(error.response.data.detail);
  }
}

async function renameFile(selectedFile, newName, setFiles, files) {
  try {
    const fileExtension = selectedFile.file_name.split('.')[1]; 
    const newFileName = `${newName}.${fileExtension}`; 

    const response = await axios.patch(`files/rename/${selectedFile.file_id}/${newFileName}`, newFileName, {
      headers: {
        'Authorization': `Bearer ${access_token}`
      }
    });
    console.log(response.data)

    const updatedFiles = files.map((file) => {
      if (file.file_id === selectedFile.file_id) {
        return { ...file, file_name: newFileName };
      } else {
        return file;
      }
    });
    setFiles(updatedFiles);
  } catch (error) {
    console.log(error.response.data.detail);
  }
}

async function deleteFile(selectedFile, setFiles, files) {
  try {
    const response = await axios.delete(`files/delete/${selectedFile.file_id}`, {
      headers: {
        'Authorization': `Bearer ${access_token}`
      }
    });
    setFiles(files.filter(file => file.file_id !== selectedFile.file_id));
    console.log(response.data)
  } catch (error) {
    console.log(error.response.data.detail);
  }
}

async function addToBasket(selectedFile, setFiles, files) {
  try {
    const response = await axios.patch(`basket/add/file/${selectedFile.file_id}`, {}, {
      headers: {
        'Authorization': `Bearer ${access_token}`
      }
    });
    console.log(response.data);
    setFiles(files.filter(file => file.file_id !== selectedFile.file_id));
  } catch (error) {
    console.log(error.response.data.detail);
  }
}

async function addToFavorite(selectedFile, setFiles, files) {
  try {
    const response = await axios.patch(`favorite/add/file/${selectedFile.file_id}`, {}, {
      headers: {
        'Authorization': `Bearer ${access_token}`
      }
    });
    console.log(response.data)
    setFiles(files.filter(file => file.file_id !== selectedFile.file_id));
  } catch (error) {
    console.log(error.response.data.detail);
  }
}

async function revertMovedFile(selectedFile, setFiles, files) {
  try {
    const response = await axios.patch(`revert/file/${selectedFile.file_id}`, {}, {
      headers: {
        'Authorization': `Bearer ${access_token}`
      }
    });
    console.log(response.data)
    setFiles(files.filter(file => file.file_id !== selectedFile.file_id));
  } catch (error) {
    console.log(error.response.data.detail);
  }
}

export { downloadFile, deleteFile, renameFile, addToBasket, addToFavorite, revertMovedFile };
