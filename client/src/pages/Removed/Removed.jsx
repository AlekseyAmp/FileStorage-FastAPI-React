import React from 'react'

import Category from '../../components/Category/Category'

function Removed() {
  return (
    <Category
    title={'Здесь хранятся удаленные файлы'}
    titleIcon={<img src="img/categories/delete.png" alt="removed" />}
    labelTitle = {'удаленным файлам'}
    background='rgb(243 217 220 / 60%)'
    />
  )
}

export default Removed
