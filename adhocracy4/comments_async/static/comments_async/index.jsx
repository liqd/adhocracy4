import React from 'react'
import ReactDOM from 'react-dom'

import CommentBox from './comment_box'

export function renderComment (el) {
  const props = JSON.parse(el.getAttribute('data-attributes'))
  ReactDOM.render(<CommentBox {...props} ref={(commentbox) => { window.commentbox = commentbox }} />, el)
}
