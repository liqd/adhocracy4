import React from 'react'
import django from 'django'

const Alert = ({ type, message, onClick, timer }) => {
  const closeTag = django.gettext('Close')
  if (timer) {
    setTimeout(onClick, timer)
  }
  if (type) {
    return (
      <div className={`alert alert--${type}`} role="alert" onClick={onClick}>
        <div className="l-wrapper">
          {message}
          <button className="alert__close" title={closeTag}>
            <i className="fa fa-times" aria-label={closeTag} />
          </button>
        </div>
      </div>
    )
  }

  return null
}

module.exports = Alert
