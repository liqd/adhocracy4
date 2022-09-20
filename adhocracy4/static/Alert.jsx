import React, { useRef, useEffect } from 'react'
import django from 'django'

const Alert = ({ type, message, onClick, timeInMs }) => {
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
      <div className={`alert alert--${type}`} role="alert">
        <div className="l-wrapper">
          {message}
          <button className="alert__close" title={closeTag} onClick={onClick}>
            <i className="fa fa-times" aria-label={closeTag} />
          </button>
        </div>
      </div>
    )
  }

  return null
}

module.exports = Alert
