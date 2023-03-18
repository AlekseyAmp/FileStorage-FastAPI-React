import React from 'react';

import SidebarRight from './SibebarRight/SidebarRight';
import SidebarLeft from './SidebarLeft/SidebarLeft';

function SidebarLayout(props) {
  return (
    <div className="mydisk">

        <SidebarLeft />

      <div className="content">{props.children}</div>

        <SidebarRight />

    </div>
  );
}

export default SidebarLayout;
