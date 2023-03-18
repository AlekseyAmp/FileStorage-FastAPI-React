import React from 'react'

import Category from '../../components/Category/Category'

function Favorites() {
  return (
    <Category
    title={'Здесь хранятся ваши любимые файлы'}
    titleIcon={<img src="img/categories/heart.png" alt="favorite" />}
    labelTitle = {'по избранным файлам'}
    background='rgb(196 255 229 / 60%)'
    />
  )
}

export default Favorites
