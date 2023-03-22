import React from 'react'

import Category from '../../components/Category/Category'

function Documents() {
  return (
    <Category
      categoryName={'documents'}
      imagePath='../../img/categories/docs.png'
      title={'Документы'}
      labelTitle={'документам'}
      background='rgb(220 227 245 / 60%)'
    />
  )
}

export default Documents
