import React from 'react'
import { createRoot } from 'react-dom/client'
import { initialise as ReactWidgetInit } from '../../static/widget'

import PollQuestions from './PollDetail/PollQuestions'

function init () {
  ReactWidgetInit('a4', 'open-poll',
    function (el) {
      const pollId = el.dataset.pollId
      const container = el
      const root = createRoot(container)
      root.render(
        <PollQuestions pollId={pollId} />
      )
    }
  )
}

document.addEventListener('DOMContentLoaded', init, false)
