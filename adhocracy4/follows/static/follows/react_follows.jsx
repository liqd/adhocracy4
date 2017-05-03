var FollowButton = require('./FollowButton')
var React = require('react')
var ReactDOM = require('react-dom')

module.exports.renderFollow = function (mountpoint) {
  let el = document.getElementById(mountpoint)
  let project = el.getAttribute('data-project')
  ReactDOM.render(<FollowButton project={project} />, el)
}
