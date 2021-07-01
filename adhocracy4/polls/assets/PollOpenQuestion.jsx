import React from 'react'

export const PollTextQuestion = (props) => {
  const questionHelpText = props.question.help_text ? <div className="poll__help-text">{props.question.help_text}</div> : null
  return (
    <div className="poll u-border">
      <h2>{props.question.label}</h2>
      {questionHelpText}
      <div className="poll__rows">
        <input
          className="input-group__input"
          type="text"
          name="question"
          id={'id_choice-' + props.question.id + '-open'}
          disabled={!props.question.authenticated}
          onChange={(e) => { props.onOpenChange(props.question.id, e.target.value) }}
        />
      </div>
    </div>
  )
}
