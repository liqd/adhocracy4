import React from 'react'
import { createRoot } from 'react-dom/client'

import { FollowButton } from './FollowButton'

export const renderFollow = function (el: HTMLElement) {
  const props = JSON.parse(el.getAttribute('data-attributes') as string)
  const root = createRoot(el)
  root.render(<FollowButton {...props} />)
}

export default {
  renderFollow
}
