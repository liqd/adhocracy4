import React from 'react'

interface FormFieldErrorProps {
  error?: Record<string, string> | null;
  field: string;
  id?: string;
}

const FormFieldError: React.FC<FormFieldErrorProps> = ({ error, field, id }) => {
  if (error && error[field]) {
    return (
      <p id={id} className="field-error">
        {error[field]}
      </p>
    )
  }

  return null
}

export default FormFieldError
