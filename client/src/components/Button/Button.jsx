import React from 'react'

import './Button.module.scss'

function Button({title, marginTop, onClick}) {
  return (
    <div onClick={onClick} className='button-block' style={{ marginTop }}>
      <button>
        {title}
      </button>
    </div>
  )
}

export default Button;
