import React from 'react'
import { createRoot } from 'react-dom/client'
import DocumentManagement from './DocumentManagement'

module.exports.renderDocumentManagement = function (el) {
  const chapters = JSON.parse(el.getAttribute('data-chapters'))
  const module = el.getAttribute('data-module')
  const config = JSON.parse(el.getAttribute('data-config'))
  const reloadOnSuccess = JSON.parse(el.getAttribute('data-reloadOnSuccess'))
  const root = createRoot(el)
  root.render(<DocumentManagement key={module} module={module} chapters={chapters} config={config} reloadOnSuccess={reloadOnSuccess} />, el)
}
