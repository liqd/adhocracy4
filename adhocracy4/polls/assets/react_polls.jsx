import React from 'react'
import { createRoot } from 'react-dom/client'

import { EditPollManagement } from './PollDashboard/EditPollManagement'
import PollQuestions from './PollDetail/PollQuestions'

module.exports.renderPolls = function (element) {
  const pollId = element.getAttribute('data-poll-id')
  const container = element
  const root = createRoot(container)
  root.render(<PollQuestions pollId={pollId} />)
}

module.exports.renderPollManagement = function (element) {
  const pollId = JSON.parse(element.getAttribute('data-poll-id'))

  const reloadOnSuccess = JSON.parse(element.getAttribute('data-reloadOnSuccess'))

  const root = createRoot(element)
  root.render(<EditPollManagement pollId={pollId} reloadOnSuccess={reloadOnSuccess} />)
}
