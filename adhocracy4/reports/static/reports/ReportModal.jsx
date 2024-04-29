import React, { useState } from 'react'
import django from 'django'
import Modal from '../../../static/Modal'
import api from '../../../static/api'

const translations = {
  reportSent: django.gettext('Report sent'),
  thankyouText: django.gettext('Thank you! We are taking care of it.'),
  placeholderText: django.gettext('Your message'),
  sendReport: django.gettext('Send Report')
}

export const ReportModal = (props) => {
  const [report, setReport] = useState('')
  const [showSuccessMessage, setShowSuccessMessage] = useState(false)
  const [showReportForm, setShowReportForm] = useState(true)

  const partials = {}

  const handleTextChange = (e) => {
    setReport(e.target.value)
  }

  const submitReport = () => {
    api.report.submit({
      description: report,
      content_type: props.contentType,
      object_pk: props.objectId
    })
      .done(() => {
        setReport('')
        setShowSuccessMessage(true)
        setShowReportForm(false)
      })
  }

  if (showSuccessMessage) {
    partials.title = translations.reportSent
    partials.body = (
      <div className="u-spacer-bottom-triple">
        <i className="fa fa-check" /> {translations.thankyouText}
      </div>
    )
    partials.hideFooter = true
    partials.bodyClass = 'success'
  } else if (showReportForm) {
    partials.title = translations.sendReport
    partials.description = props.description
    partials.body = (
      <div className="form-group">
        <textarea
          rows="5" className="form-control report-message" value={report}
          placeholder={translations.placeholderText} onChange={handleTextChange}
        />
      </div>
    )
  }

  return (
    <Modal
      abort={props.abort}
      name={props.name}
      handleSubmit={submitReport}
      action={translations.sendReport}
      partials={partials}
      keepOpenOnSubmit
    />
  )
}
