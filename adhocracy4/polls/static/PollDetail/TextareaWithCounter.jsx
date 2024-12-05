import React from 'react'
import django from 'django'
import { CharCounter } from './CharCounter'
import FormFieldError from '../../../static/FormFieldError'

const translated = {
  specify: django.gettext('Please specify:')
}

export const TextareaWithCounter = ({ value, onChange, disabled, error, id, questionType = 'other' }) => {
  // textarea rows and character length based on question type
  const rowSize = questionType === 'open' ? 6 : 3
  const maxLength = questionType === 'open' ? 750 : 250

  const handleDynamicHeight = (textarea) => {
    if (!textarea) return
    textarea.style.height = 'auto' // Reset height
    textarea.style.height = textarea.scrollHeight + 'px' // Adjust height based on content
  }

  const handleInputChange = (e) => {
    onChange(e)
    handleDynamicHeight(e.target)
  }

  // Only add aria-invalid when there's an error for the specific id:
  const ariaInvalid = error && error[id] && error[id].length > 0 ? 'true' : 'false'

  return (
    <div id={'textarea-with-counter-' + id} className="a4-textarea-with-counter" role="region">
      <label className="a4-sr-only" htmlFor={'id_choice-' + id + '-' + questionType}>
        {translated.specify}
      </label>
      <textarea
        className="a4-textarea-with-counter__textarea"
        name="question"
        id={'id_choice-' + id + '-' + questionType}
        value={value}
        maxLength={maxLength}
        onChange={handleInputChange}
        disabled={disabled}
        aria-invalid={ariaInvalid}
        aria-describedby={'id_error-' + id + ' id_char-count-' + id}
        rows={rowSize}
      />
      <CharCounter value={value} max={maxLength} id={'id_char-count-' + id} />
      {error && <FormFieldError id={'id_error-' + id} error={error} field={id} />}
    </div>
  )
}
