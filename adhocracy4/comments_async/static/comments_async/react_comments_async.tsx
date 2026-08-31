import React from 'react'
import { createRoot } from 'react-dom/client'

import CommentBox from './comment_box'

export function renderComment (el: HTMLElement) {
  const props = JSON.parse(el.getAttribute('data-attributes') as string)
  const root = createRoot(el)
  root.render(<CommentBox {...props} />)
}
