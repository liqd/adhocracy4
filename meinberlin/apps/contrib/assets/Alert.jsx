var React = require('react')
var django = require('django')

const Alert = ({ type, message, onClick }) => {
  if (type) {
    return (
      <div className={`alert alert--${type}`} role="alert">
        <div className="l-wrapper">
          {message}
          <button className="alert__close" title={django.gettext('Close')} onClick={onClick}>
            <i className="fa fa-times" aria-label={django.gettext('Close')} />
          </button>
        </div>
      </div>
    )
  }

  return null
}

module.exports = Alert
