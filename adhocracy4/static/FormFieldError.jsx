import React from 'react'

const FormFieldError = ({ error, field, id }) => {
  if (error && error[field]) {
    const msg = Array.isArray(error[field]) ? error[field][0] : error[field]
    return (
      <p id={id} className="field-error">{msg}</p>
    )
  }

  return null
}

module.exports = FormFieldError
