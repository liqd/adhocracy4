import React from 'react'
import { createRoot } from 'react-dom/client'

const FollowButton = require('./FollowButton')

module.exports.renderFollow = function (el) {
  const project = el.getAttribute('data-project')
  const root = createRoot(el)
  root.render(<FollowButton project={project} />)
}
