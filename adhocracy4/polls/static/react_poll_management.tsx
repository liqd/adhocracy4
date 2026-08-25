import React from 'react'
import { createRoot } from 'react-dom/client'
import { initialise as ReactWidgetInit } from '../../static/widget'

import { EditPollManagement } from './PollDashboard/EditPollManagement'

function init () {
  ReactWidgetInit('a4', 'poll-management',
    function (el: HTMLElement) {
      const props = JSON.parse(el.dataset.attributes as string)
      const root = createRoot(el)

      root.render(
        <EditPollManagement {...props} />
      )
    }
  )
}

document.addEventListener('DOMContentLoaded', init, false)