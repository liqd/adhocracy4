// DEPRECATED: this component tree is superseded by
// comments_async/static/comments_async. Kept for backwards compatibility
// with consumers still importing the legacy comments module.
import React from 'react'
import { createRoot } from 'react-dom/client'

import CommentBox from './CommentBox'

export const renderComment = function (el: HTMLElement) {
  const props = JSON.parse(el.getAttribute('data-attributes') as string)
  const root = createRoot(el)
  root.render(<CommentBox {...props} />)
}

export default {
  renderComment
}
