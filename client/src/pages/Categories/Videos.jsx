import React from 'react'

import Category from '../../components/Category/Category'

function Videos() {
  return (
    <Category
    categoryName={'videos'}
    imagePath='../../img/categories/videos.png'
    title={'Видео'}
    labelTitle = {'видео'}
    background='rgb(220 227 245 / 60%)'
    />
  )
}

export default Videos
