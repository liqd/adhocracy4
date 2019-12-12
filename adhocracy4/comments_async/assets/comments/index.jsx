import React from 'react'
import ReactDOM from 'react-dom'

import CommentBox from './comment_box'

function renderComment (el) {
  const props = JSON.parse(el.getAttribute('data-attributes'))
  ReactDOM.render(<CommentBox {...props} />, el)
}

export { renderComment }
export default renderComment
