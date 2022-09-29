import React from 'react'
import { createRoot } from 'react-dom/client'
import { widget as ReactWidget } from 'adhocracy4'
import PresentBox from './PresentBox'

function init () {
  ReactWidget.initialise('ie', 'present',
    function renderData (el) {
      const props = JSON.parse(el.getAttribute('data-attributes'))
      const root = createRoot(el)
      root.render(
        <React.StrictMode>
          <PresentBox {...props} />
        </React.StrictMode>
      )
    }
  )
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
