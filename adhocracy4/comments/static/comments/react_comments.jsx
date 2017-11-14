var CommentBox = require('./CommentBox')
var React = require('react')
var ReactDOM = require('react-dom')

module.exports.renderComment = function (el) {
  let props = JSON.parse(el.getAttribute('data-attributes'))
  ReactDOM.render(<CommentBox {...props} />, el)
}
