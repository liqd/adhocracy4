var React = require('react')
var django = require('django')

const Alert = ({ type, message, onClick }) => {
  const closeTag = django.gettext('Close')
  if (type) {
    return (
      <div className={`alert alert--${type}`} role="alert" onClick={onClick}>
        <div className="l-wrapper">
          {message}
          <button className="alert__close mr-3" title={closeTag}>
            <i className="fa fa-times" aria-label={closeTag} />
          </button>
        </div>
      </div>
    )
  }

  return null
}

module.exports = Alert
