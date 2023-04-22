import axios from '../utils/axios';
import Cookie from 'js-cookie';

const access_token = Cookie.get('access_token');

async function createCategory(categoryName) {
    try {
        const response = await axios.post(`categories/create/${categoryName}`, categoryName, {
            headers: {
                'Authorization': `Bearer ${access_token}`
            }
        });
        console.log(response.data)
    } catch (error) {
        console.log(error.response.data.detail);
    }
}

async function renameCategory(categoryName, newName) {
    try {
        const response = await axios.patch(`categories/rename/${categoryName}/${newName}`, newName, {
            headers: {
                'Authorization': `Bearer ${access_token}`
            }
        });
        console.log(response.data)
    } catch (error) {
        console.log(error.response.data.detail);
    }
}

async function deleteCategory(selectedCategory, categoryName, setCategories, categories) {
    try {
        const response = await axios.delete(`categories/delete/${categoryName}`, {
            headers: {
                'Authorization': `Bearer ${access_token}`
            }
        });
        setCategories(categories.filter(category => category.category_id !== selectedCategory.category_id));
        console.log(response.data)
    } catch (error) {
        console.log(error.response.data.detail);
    }
}

export { createCategory, deleteCategory, renameCategory };
