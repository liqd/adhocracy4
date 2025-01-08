import React, { useState, useEffect } from 'react'
import django from 'django'
import { TextareaWithCounter } from './TextareaWithCounter'

const translated = {
  other: django.gettext('other')
}

const ChoiceInput = ({
  type,
  choice,
  checked,
  onInputChange,
  disabled
}) => (
  <input
    className="poll-row__radio"
    type={type}
    id={'id_choice-' + choice.id + '-' + (type === 'radio' ? 'single' : 'multiple')}
    value={choice.id}
    checked={checked}
    onChange={(event) => onInputChange(event, choice.is_other_choice)}
    disabled={disabled}
    aria-describedby={'textarea-with-counter-' + choice.id}
  />
)

// eslint-disable-next-line react/display-name
export const ChoiceRow = React.memo(({
  choice,
  checked,
  onInputChange,
  type,
  disabled,
  otherChoiceAnswer,
  onOtherChange,
  isReadOnly,
  errors
}) => {
  const [textareaValue, setTextareaValue] = useState(otherChoiceAnswer)
  const [showTextarea, setShowTextarea] = useState(false)

  // When the choice is selected or changed, update the textarea visibility
  useEffect(() => {
    if (checked && choice.is_other_choice) {
      setShowTextarea(true)
    } else {
      setShowTextarea(false)
    }
  }, [checked, choice.is_other_choice])

  const handleChange = (event, isOtherChoice) => {
    // Update the checkbox/radio button state
    onInputChange(event, isOtherChoice)

    // If the "Other" option is selected, show the textarea
    if (isOtherChoice && event.target.checked) {
      setShowTextarea(true)
    } else {
      setShowTextarea(false)
    }
  }

  const handleTextareaChange = (event) => {
    // Preserve the value of the textarea even if options are changed
    setTextareaValue(event.target.value)
    onOtherChange(event)
  }

  return (
    <label
      className={(choice.is_other_choice ? 'poll__choice--other' : 'poll-row radio')}
      htmlFor={'id_choice-' + choice.id + '-' + (type === 'radio' ? 'single' : 'multiple')}
    >
      <ChoiceInput
        type={type}
        choice={choice}
        checked={checked}
        onInputChange={handleChange}
        disabled={disabled}
      />
      <span className={'radio__text' + (type === 'checkbox' ? ' radio__text--checkbox' : '')}>
        {choice.is_other_choice ? translated.other : choice.label}
      </span>
      {showTextarea && (
        <TextareaWithCounter
          id={choice.id}
          value={textareaValue} // Always use the local state value
          onChange={handleTextareaChange}
          disabled={disabled}
          error={errors}
        />
      )}
    </label>
  )
})
