import React from 'react'

interface ErrorListProps {
  errors?: Record<string, string[]>
  field: string
}

const ErrorList = ({ errors, field }: ErrorListProps) => {
  if (errors && errors[field]) {
    return (
      <div className="errorlist" role="alert" aria-atomic="true">
        <ul>
          {errors[field].map(function (msg, index) {
            return <li key={index}><a href="#{msg_id}">{msg}</a></li>
          })}
        </ul>
      </div>
    )
  }

  return <div role="alert" aria-atomic="true" id="error-list" />
}

export default ErrorList
