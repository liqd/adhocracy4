import React from 'react'
import { createRoot } from 'react-dom/client'

import { FollowButton } from './FollowButton'

module.exports.renderFollow = function (el) {
  const props = JSON.parse(el.getAttribute('data-attributes'))
  const root = createRoot(el)
  root.render(<FollowButton {...props} />)
}
