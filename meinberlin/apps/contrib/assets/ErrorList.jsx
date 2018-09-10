var React = require('react')

const ErrorList = ({ errors, field }) => {
  if (errors && errors[field]) {
    return (
      <ul className="errorlist">
        {errors[field].map(function (msg, index) {
          return <li key={msg}>{msg}</li>
        })}
      </ul>
    )
  }

  return null
}

module.exports = ErrorList
