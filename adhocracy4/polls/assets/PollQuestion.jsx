import React from 'react'
import django from 'django'

export const PollQuestion = (props) => {
  const multiHelpText = props.question.multiple_choice ? <div className="poll__help-text">{django.gettext('Multiple answers are possible.')}</div> : null

  return (
    <div className="poll u-border">
      <h2>{props.question.label}</h2>
      {multiHelpText}
      <div className="poll__rows">
        {
          props.question.choices.map((choice, i) => {
            const checked = props.question.userChoices.indexOf(choice.id) !== -1

            if (!props.question.multiple_choice) {
              return (
                <label className="poll-row radio" key={choice.id} htmlFor={'id_choice-' + choice.id + '-single'}>
                  <input
                    className="poll-row__radio radio__input"
                    type="radio"
                    name="question"
                    id={'id_choice-' + choice.id + '-single'}
                    value={choice.id}
                    checked={checked}
                    onChange={(e) => { props.onSingleChange(props.question.id, e.target.value) }}
                    disabled={!props.question.authenticated}
                  />
                  <span className="radio__text">{choice.label}</span>
                  {choice.is_other_choice &&
                    <input
                      className="input-group__input"
                      type="text"
                      name="question"
                      id={'id_choice-' + choice.id + '-single'}
                      onChange={(e) => { props.onOtherChange(props.question.id, e.target.value) }}
                      disabled={!props.question.authenticated}
                    />}
                </label>
              )
            } else {
              return (
                <label className="poll-row radio" key={choice.id} htmlFor={'id_choice-' + choice.id + '-multiple'}>
                  <input
                    className="poll-row__radio radio__input"
                    type="checkbox"
                    name="question"
                    id={'id_choice-' + choice.id + '-multiple'}
                    value={choice.id}
                    checked={checked}
                    onChange={(e) => { props.onMultiChange(props.question.id, e.target.value) }}
                    disabled={!props.question.authenticated}
                  />
                  <span className="radio__text radio__text--checkbox">{choice.label}</span>
                  {choice.is_other_choice &&
                    <input
                      className="input-group__input"
                      type="text"
                      name="question"
                      id={'id_choice-' + choice.id + '-single'}
                      onChange={(e) => { props.onOtherChange(props.question.id, e.target.value) }}
                      disabled={!props.question.authenticated}
                    />}
                </label>
              )
            }
          })
        }
      </div>
    </div>
  )
}
