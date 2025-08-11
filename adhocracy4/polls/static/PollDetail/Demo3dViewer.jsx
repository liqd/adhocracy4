import React, { useEffect, useState } from 'react'
import django from 'django'
import * as OV from 'online-3d-viewer'

export const Demo3dViewer = () => {
  const [mIndex, setIndex] = useState(0)
  const models = ['/static/images/billboard.glb', '/static/images/rhino.glb']

  const [currentModel, setCurrentModel] = useState(models[0])

  useEffect(() => {
    // This code will run after the component mounts (equivalent to window load event)
    OV.Init3DViewerElements()
  }, [mIndex]) // Empty dependency array means this runs once after initial render

  return (
    <div>
      <h3>Beautiful 3d viewer </h3>
      <div
        className="online_3d_viewer"
        style={{ width: '100%', height: '600px' }}
            // model="/static/images/billboard.glb"
        model="/static/images/tree.glb"
      />
    </div>
  )
}
