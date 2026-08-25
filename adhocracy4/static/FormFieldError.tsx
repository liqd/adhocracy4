import React from 'react'

interface FormFieldErrorProps {
  error?: Record<string, unknown>
  field: string
  id?: string
}

const FormFieldError = ({ error, field, id }: FormFieldErrorProps) => {
  if (error && error[field]) {
    const msg = Array.isArray(error[field]) ? error[field][0] : error[field]
    return (
      <p id={id} className="field-error">{String(msg)}</p>
    )
  }

  return null
}

export default FormFieldError
