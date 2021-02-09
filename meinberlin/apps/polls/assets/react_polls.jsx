const React = require('react')
const ReactDOM = require('react-dom')
const Question = require('./Question')
const PollManagement = require('./PollManagement')

module.exports.renderPolls = function (element) {
  const question = JSON.parse(element.getAttribute('data-question'))
  const module = element.getAttribute('data-module')

  ReactDOM.render(<Question module={module} question={question} />, element)
}

module.exports.renderPollManagement = function (element) {
  const poll = JSON.parse(element.getAttribute('data-poll'))
  const module = element.getAttribute('data-module')

  const reloadOnSuccess = JSON.parse(element.getAttribute('data-reloadOnSuccess'))

  ReactDOM.render(<PollManagement module={module} poll={poll} reloadOnSuccess={reloadOnSuccess} />, element)
}
