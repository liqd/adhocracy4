const CommentBox = require('./CommentBox')
const React = require('react')
const ReactDOM = require('react-dom')

module.exports.renderComment = function (el) {
  const props = JSON.parse(el.getAttribute('data-attributes'))
  ReactDOM.render(<CommentBox {...props} />, el)
}
