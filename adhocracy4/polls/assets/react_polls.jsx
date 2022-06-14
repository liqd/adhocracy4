import React from 'react'
import { createRoot } from 'react-dom/client'

import { EditPollQuestions } from './EditPollQuestions'
import PollQuestions from './PollQuestions'

module.exports.renderPolls = function (element) {
  const pollId = element.getAttribute('data-poll-id')
  const container = element
  const root = createRoot(container)
  root.render(
    <React.StrictMode>
      <PollQuestions pollId={pollId} />
    </React.StrictMode>
  )
}

module.exports.renderPollManagement = function (element) {
  const pollId = JSON.parse(element.getAttribute('data-poll-id'))

  const reloadOnSuccess = JSON.parse(element.getAttribute('data-reloadOnSuccess'))

  const root = createRoot(element)
  root.render(
    <React.StrictMode>
      <EditPollQuestions pollId={pollId} reloadOnSuccess={reloadOnSuccess} />
    </React.StrictMode>
  )
}
