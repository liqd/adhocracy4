import React, { useState } from 'react'

export const PollOpenQuestion = (props) => {
  const questionHelpText = props.question.help_text ? <div className="poll__help-text">{props.question.help_text}</div> : null
  const [openAnswer, setOpenAnswer] = useState(props.question.open_answer)

  const handleOpenChange = (event) => {
    setOpenAnswer(event.target.value)
    props.onOpenChange(props.question.id, openAnswer)
  }

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
          onChange={(event) => { handleOpenChange(event) }}
        />
      </div>
    </div>
  )
}
