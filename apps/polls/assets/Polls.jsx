var React = require('react')
var ReactDOM = require('react-dom')
var Question = require('./Question')
var PollManagement = require('./PollManagement')

module.exports.renderPolls = function (mountpoint) {
  let element = document.getElementById(mountpoint)

  let question = JSON.parse(element.getAttribute('data-question'))

  ReactDOM.render(<Question question={question} />, element)
}

module.exports.renderPollManagement = function (mountpoint) {
  let element = document.getElementById(mountpoint)

  let poll = JSON.parse(element.getAttribute('data-poll'))
  let module = element.getAttribute('data-module')

  ReactDOM.render(<PollManagement module={module} poll={poll} />, element)
}
