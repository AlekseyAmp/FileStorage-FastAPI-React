import React from "react";

import MovedFiles from "../../components/MovedFiles/MovedFiles"

function Favoties() {
  return (
    <div>
      <MovedFiles
        url={'get_favorites_files'}
        title={'Здесь хранятся ваши любимые файлы'}
        titleIcon={<img src="img/categories/heart.png" alt="favorite" />}
        labelTitle = {'по избранным файлам'}
        background='rgb(196 255 229 / 60%)'
      />
    </div>
  );
};

export default Favoties;
