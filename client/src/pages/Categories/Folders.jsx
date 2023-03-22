import React from 'react'

import Category from '../../components/Category/Category'

function Folders() {
  return (
    <Category
    categoryName={'folders'}
    imagePath='../../img/categories/folder.png'
    title={'Папки'}
    labelTitle = {'папкам'}
     background='rgb(220 227 245 / 60%)'
     />
  )
}

export default Folders
