import { useState } from "react";

export function useContextMenu() {
  const [selectedItem, setSelectedItem] = useState(null);
  const [showContextMenuForItem, setShowContextMenuForItem] = useState(false);
  const [contextMenuPosition, setContextMenuPosition] = useState({ x: 0, y: 0 });

  function handleContextMenuForItem(e, item) {
    e.preventDefault();
    setSelectedItem(item);
    setShowContextMenuForItem(true);
    setContextMenuPosition({ x: e.pageX, y: e.pageY });
  }

  const handleCloseContextMenu = () => {
      setShowContextMenuForItem(false);
  };
  
  return {
    selectedItem,
    setSelectedItem,
    showContextMenuForItem,
    setShowContextMenuForItem,
    contextMenuPosition,
    setContextMenuPosition,
    handleContextMenuForItem,
    handleCloseContextMenu,
  };
}
