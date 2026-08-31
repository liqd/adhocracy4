import React from 'react'
import { createRoot } from 'react-dom/client'
import { initialise as ReactWidgetInit } from '../../static/widget'

import PollQuestions from './PollDetail/PollQuestions'

function init () {
  ReactWidgetInit('a4', 'polls',
    function (el: HTMLElement) {
      const props = JSON.parse(el.dataset.attributes as string)
      const root = createRoot(el)
      root.render(
        <PollQuestions {...props} />
      )
    }
  )
}

document.addEventListener('DOMContentLoaded', init, false)