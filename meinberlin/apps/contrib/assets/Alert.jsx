const React = require('react')
const django = require('django')
const closeStr = django.gettext('Close')

const Alert = ({ type, message, onClick }) => {
  if (type) {
    return (
      <div className={`alert alert--${type}`} role="alert">
        <div className="l-wrapper">
          {message}
          <button className="alert__close" title={closeStr} onClick={onClick}>
            <i className="fa fa-times" aria-label={closeStr} />
          </button>
        </div>
      </div>
    )
  }

  return null
}

module.exports = Alert
