import React from 'react'
import Link from 'react-router-dom'

function Main() {
  return (
    <div>
        <Link to='/register'>Регистрация</Link>
        <Link to='/login'>Вход</Link>
    </div>
  )
}

export default Main
