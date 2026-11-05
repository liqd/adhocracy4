import React from 'react'
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
  disabled,
  name,
  isResult = false
}) => (
  <div className="poll-choice__input-wrapper">
    {!isResult
      ? (
        <input
          className="poll-choice__input"
          type={type}
          id={'id_choice-' + choice.id + '-' + (type === 'radio' ? 'single' : 'multiple')}
          name={name}
          value={choice.id}
          checked={checked}
          onChange={(event) => onInputChange(event, choice.is_other_choice)}
          disabled={disabled}
          aria-describedby={'textarea-with-counter-' + choice.id}
        />
        )
      : (
        <div className="poll-choice__result-icon">
          {checked
            ? (
              <i className="fas fa-check-circle poll-choice__check-icon" />
              )
            : (
              <div className="poll-choice__empty-circle" />
              )}
        </div>
        )}
  </div>
)

export const ChoiceRow = React.memo(({
  choice,
  checked,
  onInputChange,
  type,
  disabled,
  otherChoiceAnswer,
  onOtherChange,
  errors,
  name,
  isResult = false,
  review = false,
  percent = null
}) => {
  const textareaValue = otherChoiceAnswer || ''
  const showTextarea = checked && choice.is_other_choice

  const handleChange = (event, isOtherChoice) => {
    if (isResult) return
    onInputChange?.(event, isOtherChoice)
  }

  const classes = [
    'poll-choice',
    checked ? 'poll-choice--checked' : '',
    choice.is_other_choice ? 'poll-choice--other' : '',
    isResult ? 'poll-choice--result' : '',
    review ? 'poll-choice--review' : ''
  ].filter(Boolean).join(' ')

  return (
    <label
      className={classes}
      htmlFor={!isResult ? ('id_choice-' + choice.id + '-' + (type === 'radio' ? 'single' : 'multiple')) : undefined}
    >
      {isResult && percent !== null && (
        <div
          className="poll-choice__fill"
          style={{ width: percent + '%' }}
        />
      )}

      <div className="poll-choice__container">
        <ChoiceInput
          type={type}
          choice={choice}
          checked={checked}
          onInputChange={handleChange}
          disabled={disabled || isResult}
          name={name}
          isResult={isResult}
        />
        <span className="poll-choice__label">
          {choice.is_other_choice ? translated.other : choice.label}
        </span>
        {isResult && percent !== null && (
          <span className="poll-choice__percentage">{percent}%</span>
        )}
      </div>

      {showTextarea && !isResult && (
        <div className="poll-choice__textarea-container">
          <TextareaWithCounter
            id={choice.id}
            value={textareaValue}
            onChange={onOtherChange}
            disabled={disabled}
            error={errors}
            label={translated.other}
          />
        </div>
      )}
    </label>
  )
})

ChoiceRow.displayName = 'ChoiceRow'
