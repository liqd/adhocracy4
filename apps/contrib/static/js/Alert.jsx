/* global django */

var React = require('react')

const Alert = ({type, message, onClick}) => {
  if (type) {
    return (
      <div className={`alert ${type}`} role="alert" onClick={onClick}>
        <div className="l-wrapper">
          {message}
          <button className="alert__close" title={django.gettext('Close')}>
            <i className="fa fa-times" aria-hidden="true" />
          </button>
        </div>
      </div>
    )
  }

  return null
}

module.exports = Alert
