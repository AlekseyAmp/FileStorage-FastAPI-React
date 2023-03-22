import React from 'react'

import Category from '../../components/Category/Category'

function Images() {
  return (
    <Category
    categoryName={'images'}
    imagePath='../../img/categories/image.png'
    title={'Изображения'}
    labelTitle = {'изображениям'}
     background='rgb(220 227 245 / 60%)'
     />
  )
}

export default Images
