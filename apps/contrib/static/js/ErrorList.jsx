var React = require('react')

const ErrorList = ({errors}) => {
  if (errors && errors.label) {
    return (
      <ul className="errorlist">
        {errors.label.map(function (msg, index) {
          return <li key={msg}>{msg}</li>
        })}
      </ul>
    )
  }

  return null
}

module.exports = ErrorList
