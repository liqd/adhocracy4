import React, { useState } from 'react'
import django from 'django'
import api from '../../../static/api'
import Modal from '../../../static/Modal'

const translations = {
  reportTitle: django.gettext('Report Content'),
  reportSent: django.gettext('Report sent'),
  thankyouText: django.gettext('Thank you! We are taking care of it.'),
  placeholderText: django.gettext('Your message'),
  sendReport: django.gettext('Send Report'),
  report: django.gettext('Report'),
  validationError: django.gettext('Please enter a message before submitting.')
}

export const ReportModal = (props) => {
  const [report, setReport] = useState('')
  const [showSuccessMessage, setShowSuccessMessage] = useState(false)
  const [showReportForm, setShowReportForm] = useState(true)
  const [validationError, setValidationError] = useState(false)

  const partials = {}

  const handleTextChange = (e) => {
    setReport(e.target.value)
    // Clear validation error when user starts typing
    if (validationError) {
      setValidationError(false)
    }
  }

  const submitReport = () => {
    // Validate before submitting
    if (!report.trim()) {
      setValidationError(true)
      return
    }

    api.report.submit({
      description: report,
      content_type: props.contentType,
      object_pk: props.objectId
    })
      .done(() => {
        setReport('')
        setShowSuccessMessage(true)
        setShowReportForm(false)
        setValidationError(false)
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
    partials.title = translations.reportTitle
    partials.description = props.description
    partials.body = (
      <div className="form-group">
        <textarea
          rows="5"
          className={'form-control report-message' + (validationError ? ' is-invalid' : '')}
          value={report}
          placeholder={translations.placeholderText}
          onChange={handleTextChange}
        />
        {validationError && (
          <div className="message message--error">
            {translations.validationError}
          </div>
        )}
      </div>
    )
  }

  return (
    <Modal
      partials={partials}
      handleSubmit={submitReport}
      action={translations.sendReport}
      keepOpenOnSubmit
      toggle={<><i className="fas fa-exclamation-triangle" aria-hidden="true" /> {translations.report}</>}
    />
  )
}
