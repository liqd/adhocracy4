import React, { useRef, useEffect } from 'react'
import django from 'django'

const Alert = ({ type, alertAttribute, message, onClick, timeInMs }) => {
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
  if (type) {
    return (
      <div
        id="alert"
        className={'alert alert--' + type}
        aria-atomic="true"
        aria-live={alertAttribute}
      >
        <div className="container">
          {message}
          <button className="alert__close" title={closeTag} onClick={onClick}>
            <i className="fa fa-times" aria-label={closeTag} />
          </button>
        </div>

      </div>
    )
  }

  return <div aria-live="assertive" aria-atomic="true" id="alert" />
}

module.exports = Alert
