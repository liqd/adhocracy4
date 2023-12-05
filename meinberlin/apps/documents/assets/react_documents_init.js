import React from 'react'
import { createRoot } from 'react-dom/client'
import { widget as ReactWidget } from 'adhocracy4'

import DocumentManagement from './DocumentManagement'

function init () {
  ReactWidget.initialise('mb', 'document-management', (el) => {
    const props = JSON.parse(el.dataset.attributes)
    const root = createRoot(el)
    root.render(
      <React.StrictMode>
        <DocumentManagement {...props} />
      </React.StrictMode>
    )
  })
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
