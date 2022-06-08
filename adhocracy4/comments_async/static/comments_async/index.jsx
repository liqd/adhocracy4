import React from 'react'
import { createRoot } from 'react-dom/client'

import CommentBox from './comment_box'

export function renderComment (el) {
  const props = JSON.parse(el.getAttribute('data-attributes'))
  const container = el
  const root = createRoot(container)
  root.render(<CommentBox {...props} ref={(commentbox) => { window.commentbox = commentbox }} />)
}
