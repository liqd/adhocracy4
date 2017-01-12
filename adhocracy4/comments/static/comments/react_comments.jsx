var CommentBox = require('./CommentBox')
var React = require('react')
var ReactDOM = require('react-dom')

module.exports.renderComment = function (mountpoint, props) {
  ReactDOM.render(<CommentBox {...props} />, document.getElementById(mountpoint))
}
