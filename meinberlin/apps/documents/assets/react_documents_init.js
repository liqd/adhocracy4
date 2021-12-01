import * as ReactDocuments from './react_documents.jsx'
import { widget as ReactWidget } from 'adhocracy4'

function init () {
  ReactWidget.initialise('mb', 'document-management', ReactDocuments.renderDocumentManagement)
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
