var React = require('react')
var ReactDOM = require('react-dom')
var Question = require('./Question')
var PollManagement = require('./PollManagement')

module.exports.renderPolls = function (element) {
  let question = JSON.parse(element.getAttribute('data-question'))
  let module = element.getAttribute('data-module')

  ReactDOM.render(<Question module={module} question={question} />, element)
}

module.exports.renderPollManagement = function (element) {
  let poll = JSON.parse(element.getAttribute('data-poll'))
  let module = element.getAttribute('data-module')

  const reloadOnSuccess = JSON.parse(element.getAttribute('data-reloadOnSuccess'))

  ReactDOM.render(<PollManagement module={module} poll={poll} reloadOnSuccess={reloadOnSuccess} />, element)
}
