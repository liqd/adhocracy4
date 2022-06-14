import React from 'react'
import { createRoot } from 'react-dom/client'

const CommentBox = require('./CommentBox')

module.exports.renderComment = function (el) {
  const props = JSON.parse(el.getAttribute('data-attributes'))
  const root = createRoot(el)
  root.render(
    <React.StrictMode>
      <CommentBox {...props} />
    </React.StrictMode>
  )
}
