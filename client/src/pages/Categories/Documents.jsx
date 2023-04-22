import React from 'react'

import Category from '../../components/DefaultCategory/DefaultCategory'

function Documents() {
  return (
    <Category
      url={'categories/files/documents'}
      title={'Документы'}
      labelTitle={'документам'}
      background='rgb(220 227 245 / 60%)'
    />
  )
}

export default Documents;
