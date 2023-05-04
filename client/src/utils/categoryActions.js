import axios from '../utils/axios';

async function createCategory(categoryName, setCategories, categories, access_token) {
  try {
    const response = await axios.post(`categories/create/${categoryName}`, categoryName, {
      headers: {
        'Authorization': `Bearer ${access_token}`
      }
    });
    console.log(response.data)
    const newCategory = response.data;
    setCategories([...categories, newCategory]);
    const updatedResponse = await axios.get(`/categories`, {
      headers: {
        Authorization: `Bearer ${access_token}`,
      },
    });
    setCategories(updatedResponse.data);
  } catch (error) {
    console.log(error.response.data.detail);
  }
}

async function renameCategory(selectedCategory, newName, setCategories, categories, access_token) {
  try {
    const response = await axios.patch(`categories/rename/${selectedCategory.category_name}/${newName}`, newName, {
      headers: {
        'Authorization': `Bearer ${access_token}`
      }
    });
    console.log(response.data)
    const updatedCategories = categories.map((category) => {
      if (category.category_name === selectedCategory.category_name) {
        return { ...category, category_name: newName };
      } else {
        return category;
      }
    });
    setCategories(updatedCategories);
  } catch (error) {
    console.log(error.response.data.detail);
  }
}

async function deleteCategory(selectedCategory, setCategories, categories, access_token) {
  try {
    const response = await axios.delete(`categories/delete/${selectedCategory.category_name}`, {
      headers: {
        'Authorization': `Bearer ${access_token}`
      }
    });
    setCategories(categories.filter(category => category.category_name !== selectedCategory.category_name));
    console.log(response.data)
  } catch (error) {
    console.log(error.response.data.detail);
  }
}

export { createCategory, deleteCategory, renameCategory };
