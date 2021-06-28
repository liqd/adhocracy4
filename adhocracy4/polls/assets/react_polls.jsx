import { EditPollQuestions } from './EditPollQuestions'
const React = require('react')
const ReactDOM = require('react-dom')
const { PollQuestions } = require('./PollQuestions')

module.exports.renderPolls = function (element) {
  const pollId = element.getAttribute('data-poll-id')

  ReactDOM.render(<PollQuestions pollId={pollId} />, element)
}

module.exports.renderPollManagement = function (element) {
  const pollId = JSON.parse(element.getAttribute('data-poll-id'))

  const reloadOnSuccess = JSON.parse(element.getAttribute('data-reloadOnSuccess'))

  ReactDOM.render(<EditPollQuestions pollId={pollId} reloadOnSuccess={reloadOnSuccess} />, element)
}
