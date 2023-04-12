import React from 'react'
import { createRoot } from 'react-dom/client'
import { initialise as ReactWidgetInit } from '../../static/widget'

import { EditPollManagement } from './PollDashboard/EditPollManagement'

function init () {
  ReactWidgetInit('a4', 'poll-management',
    function (el) {
      const pollId = el.dataset.pollId
      const root = createRoot(el)

      const reloadOnSuccess = JSON.parse(el.getAttribute('data-reloadOnSuccess'))

      root.render(
        <EditPollManagement pollId={pollId} reloadOnSuccess={reloadOnSuccess} />
      )
    }
  )
}

document.addEventListener('DOMContentLoaded', init, false)
