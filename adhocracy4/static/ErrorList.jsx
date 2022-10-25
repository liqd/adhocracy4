import React from 'react'

const ErrorList = ({ errors, field }) => {
  if (errors && errors[field]) {
    return (
      <p className="errorlist" role="alert" aria-atomic="true">
        <ul>
          {errors[field].map(function (msg, index) {
            return <li key={index}><a href="#{msg_id}">{msg}</a></li>
          })}
        </ul>
      </p>
    )
  }

  return <p role="alert" aria-atomic="true" id="error-list" />
}

module.exports = ErrorList
