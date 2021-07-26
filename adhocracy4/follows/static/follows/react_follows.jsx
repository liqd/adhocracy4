const FollowButton = require('./FollowButton')
const React = require('react')
const ReactDOM = require('react-dom')

module.exports.renderFollow = function (el) {
  const project = el.getAttribute('data-project')
  ReactDOM.render(<FollowButton project={project} />, el)
}
