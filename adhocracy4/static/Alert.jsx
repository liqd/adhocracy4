import React from 'react'
import django from 'django'

export const Alert = ({ type, message, onClick }) => {
  const closeTag = django.gettext('Close')
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
