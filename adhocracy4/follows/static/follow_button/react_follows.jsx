var FollowButton = require('./FollowButton')
var React = require('react')
var ReactDOM = require('react-dom')

module.exports.renderFollow = function (el) {
  let project = el.getAttribute('data-project')
  ReactDOM.render(<FollowButton project={project} />, el)
}
