var React = require('react')

const Alert = ({type, message}) => {
  if (type) {
    return (
      <p className={`alert ${type}`}>
        {message}
      </p>
    )
  }

  return null
}

module.exports = Alert
