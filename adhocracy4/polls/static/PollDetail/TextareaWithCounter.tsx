import React, { useEffect, useRef } from 'react'
import django from 'django'
import { CharCounter } from './CharCounter'
import FormFieldError from '../../../static/FormFieldError'

const translated = {
  specify: django.gettext('Please specify:')
}

interface TextareaWithCounterProps {
  value: string
  onChange: (event: React.ChangeEvent<HTMLTextAreaElement>) => void
  disabled: boolean
  error?: any
  id: number | string
  questionType?: string
  label?: string
}

export const TextareaWithCounter = ({ value, onChange, disabled, error, id, questionType = 'other' }: TextareaWithCounterProps) => {
  // textarea rows and character length based on question type
  const rowSize = questionType === 'open' ? 6 : 3
  const maxLength = questionType === 'open' ? 750 : 250
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const handleDynamicHeight = (textarea: HTMLTextAreaElement | null) => {
    if (!textarea) return
    textarea.style.height = 'auto'
    textarea.style.height = textarea.scrollHeight + 'px'
  }

  useEffect(() => {
    handleDynamicHeight(textareaRef.current)
  }, [value])

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
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
        ref={textareaRef}
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
      {error && <FormFieldError id={'id_error-' + id} error={error} field={String(id)} />}
    </div>
  )
}