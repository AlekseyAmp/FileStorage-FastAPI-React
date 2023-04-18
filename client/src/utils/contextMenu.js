import { useState } from "react";

export function useContextMenu() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [showContextMenu, setShowContextMenu] = useState(false);
  const [contextMenuPosition, setContextMenuPosition] = useState({ x: 0, y: 0 });

  function handleContextMenu(e, file) {
    e.preventDefault();
    setSelectedFile(file);
    setShowContextMenu(true);
    setContextMenuPosition({ x: e.pageX, y: e.pageY });
  }

  function handleCloseContextMenu(e) {
    e.preventDefault();
    setShowContextMenu(false);
  }

  return {
    selectedFile,
    setSelectedFile,
    showContextMenu,
    setShowContextMenu,
    contextMenuPosition,
    setContextMenuPosition,
    handleContextMenu,
    handleCloseContextMenu,
  };
}
