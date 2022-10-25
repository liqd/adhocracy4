import React from 'react'

const FormFieldError = ({ error, field, id }) => {
  if (error && error[field]) {
    return (
      <p id={id} className="field-error">{error[field]}</p>
    )
  }

  return null
}

module.exports = FormFieldError
