import React from 'react'
import { createRoot } from 'react-dom/client'
import { widget as ReactWidget } from 'adhocracy4'
import QuestionBox from './QuestionBox'

function init () {
  ReactWidget.initialise('ie', 'questions',
    function (el) {
      const props = JSON.parse(el.getAttribute('data-attributes'))
      const root = createRoot(el)
      root.render(
        <React.StrictMode>
          <QuestionBox {...props} />
        </React.StrictMode>
      )
    }
  )
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
