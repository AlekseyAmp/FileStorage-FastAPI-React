import React from 'react'

import Category from '../../components/DefaultCategory/DefaultCategory'

function Music() {
  return (
    <Category
     url={'categories/files/music'}
     title={'Музыка'}
     labelTitle = {'музыке'}
     background='rgb(220 227 245 / 60%)'
     />
  )
}

export default Music;
