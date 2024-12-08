import React, { useState } from 'react'
import { CharCounter } from './CharCounter'

export const PollOpenQuestion = (props) => {
  // | Function to define state

  const getUserOpenAnswer = () => {
    const userAnswerId = props.question.userAnswer
    const userAnswer = props.question.answers.find(oa => oa.id === userAnswerId)
    return props.question.open_answer
      ? props.question.open_answer
      : ((userAnswerId && userAnswer)
          ? userAnswer.answer
          : ''
        )
  }

  const [userAnswer, setUserAnswer] = useState(getUserOpenAnswer())
  const questionHelpText = props.question.help_text ? <div className="poll__help-text">{props.question.help_text}</div> : null
  const maxlength = 750
  const userAllowedVote = props.question.authenticated || props.allowUnregisteredUsers

  const handleOpenChange = (event) => {
    setUserAnswer(event.target.value)
    props.onOpenChange(props.question.id, event.target.value)
  }

  return (
    <div className="poll poll--question">
      <h2>{props.question.label}</h2>
      {questionHelpText}
      <div className="poll__rows">
        <textarea
          className="form-control"
          name="question"
          id={'id_choice-' + props.question.id + '-open'}
          value={userAnswer}
          disabled={!userAllowedVote || props.question.isReadOnly}
          onChange={(event) => { handleOpenChange(event) }}
          maxLength={maxlength}
        />
        <div className="poll__char-counter">
          <CharCounter value={userAnswer} max={maxlength} />
        </div>
      </div>
    </div>
  )
}
