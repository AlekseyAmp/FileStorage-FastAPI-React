import React from "react";

import MovedItems from "../../components/MovedItems/MovedItems"

function Favorite() {
  return (
    <div>
      <MovedItems
        url={'favorite'}
        title={'Здесь хранятся ваши любимые файлы'}
        titleIcon={<img src="img/categories/heart.png" alt="favorite" />}
        labelTitle = {'по избранным файлам'}
        background='rgb(196 255 229 / 60%)'
        contextMenuBack='Убрать из избранного'
        isFavorite={true}
      />
    </div>
  );
};

export default Favorite;
