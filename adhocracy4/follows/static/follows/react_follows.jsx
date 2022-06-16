import React from 'react'
import ReactDOM from 'react-dom'
import FollowButton from './FollowButton'

module.exports.renderFollow = function (el) {
  const project = el.getAttribute('data-project')
  ReactDOM.render(<FollowButton project={project} />, el)
}
