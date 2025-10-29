import React, { useRef, useEffect } from 'react'
import django from 'django'

const Alert = ({ type = 'info', title, message, htmlMessage, onClick, timeInMs }) => {
  const timer = useRef()
  const closeTag = django.gettext('Close')

  useEffect(() => {
    if (timeInMs) {
      timer.current = setTimeout(onClick, timeInMs)
      return () => {
        clearTimeout(timer.current)
      }
    }
  }, [timeInMs, onClick])

  // Only check for message or htmlMessage now since type has a default
  if (!message && !htmlMessage) {
    return null
  }

  // Use alert role for danger/warning, status for others
  const ariaRole = ['danger', 'warning'].includes(type) ? 'alert' : 'status'

  return (
    <div
      id="alert"
      role={ariaRole}
      className={'alert alert--' + type}
      aria-atomic="true"
    >
      <div className="alert__content">
        {title && <h3 className="alert__headline">{title}</h3>}
        {htmlMessage
          ? (<div dangerouslySetInnerHTML={{ __html: htmlMessage }} />)
          : (message)}
      </div>
      {onClick && (
        <button
          type="button"
          className="alert__close"
          aria-label={closeTag}
          onClick={onClick}
        >
          <span className="fa fa-times" aria-hidden="true" />
        </button>
      )}
    </div>
  )
}

module.exports = Alert
