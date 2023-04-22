import React from "react";

import MovedItems from "../../components/MovedItems/MovedItems"

function Basket() {
  return (
    <div>
      <MovedItems
        url={'basket'}
        title={'Здесь хранятся ваши удалённые файлы'}
        titleIcon={<img src="img/categories/delete.png" alt="removed" />}
        labelTitle={'удаленным файлам'}
        background='rgb(243 217 220 / 60%)'
        contextMenuBack='Убрать из корзины'
        isFavorite={false}
      />
    </div>
  );
};

export default Basket;
