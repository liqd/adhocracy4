import django from 'django'
import React from 'react'
import { createRoot } from 'react-dom/client'

import { ReportModal } from './ReportModal'

module.exports.ReportModal = ReportModal

module.exports.renderReports = function (el) {
  const props = JSON.parse(el.getAttribute('data-attributes'))
  const root = createRoot(el)

  root.render(
    <ReportModal
      name={props.modalName}
      description={django.gettext('Do you want to report this content? Your message will be sent to our moderation team. They will review the reported content, and if it violates our discussion rules (netiquette), it will be removed.')}
      objectId={props.objectId}
      contentType={props.contentType}
    />)
}
