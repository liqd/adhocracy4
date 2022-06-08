import React from 'react'
import { createRoot } from 'react-dom/client'

const CommentBox = require('./CommentBox')

module.exports.renderComment = function (el) {
  const props = JSON.parse(el.getAttribute('data-attributes'))
  const container = el
  const root = createRoot(container)
  root.render(<CommentBox {...props} />)
}
