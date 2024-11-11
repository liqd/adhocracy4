import React from 'react'
import { createRoot } from 'react-dom/client'
import { initialise as ReactWidgetInit } from '../../static/widget'

import { EditPollManagement } from './PollDashboard/EditPollManagement'

function init () {
  ReactWidgetInit('a4', 'poll-management',
    function (el) {
      const props = JSON.parse(el.dataset.attributes)
      const root = createRoot(el)

      root.render(
        <EditPollManagement {...props} />
      )
    }
  )
}

document.addEventListener('DOMContentLoaded', init, false)
