import React from 'react'

import Category from '../../components/Category/Category'

function Music() {
  return (
    <Category
     categoryName={'/music'}
     title={'Музыка'}
     labelTitle = {'музыке'}
     background='rgb(220 227 245 / 60%)'
     />
  )
}

export default Music
