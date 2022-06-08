import React from 'react'
import { createRoot } from 'react-dom/client'

import FollowButton from './FollowButton'

module.exports.renderFollow = function (el) {
  const project = el.getAttribute('data-project')
  const container = el
  const root = createRoot(container)
  root.render(<FollowButton project={project} />)
}
