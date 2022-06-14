import React from 'react'
import { createRoot } from 'react-dom/client'

import FollowButton from './FollowButton'

module.exports.renderFollow = function (el) {
  const project = el.getAttribute('data-project')
  const root = createRoot(el)
  root.render(
    <React.StrictMode>
      <FollowButton project={project} />
    </React.StrictMode>
  )
}
