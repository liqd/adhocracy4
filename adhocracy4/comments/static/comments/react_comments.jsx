import React from 'react'
import ReactDOM from 'react-dom'

import CommentBox from './CommentBox'

module.exports.renderComment = function (el) {
  const props = JSON.parse(el.getAttribute('data-attributes'))
  ReactDOM.render(<CommentBox {...props} />, el)
}
