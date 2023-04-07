import React, { useState, useEffect } from "react";
import axios from "../../axios";

import File from "../../components/File/File";

import Cookies from "js-cookie";

function Basket() {
  const [files, setFiles] = useState([]);
  const access_token = Cookies.get('access_token')


  useEffect(() => {
    async function getBasketFiles() {
      try {
        const response = await axios.get("/get_basket_files", {
          headers: {
            Authorization: `Bearer ${access_token}`
          }
        });
        setFiles(response.data);
      } catch (error) {
        console.error(error);
      }
    };
    getBasketFiles();
  }, []);

  return (
    <div>
        {files.map((file) => (
          <File
          key={file.file_id}
          onContextMenu={null}
          image={`../img/categories/${file.content_type}.png`}
          name={file.name}
          size={`${Math.floor(file.size / 1000)} КБ`}
        />
        ))}
    </div>
  );
};

export default Basket;
