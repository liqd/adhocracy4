import React, { useEffect, useState } from 'react'
import django from 'django'

export const PollQuestion = (props) => {
  const getUserAnswer = () => {
    const userAnswerId = props.question.other_choice_user_answer
    const userAnswer = props.question.other_choice_answers.find(oc => oc.vote_id === userAnswerId)
    return (userAnswerId && userAnswer)
      ? userAnswer.answer
      : ''
  }

  const multiHelpText = props.question.multiple_choice ? <div className="poll__help-text">{django.gettext('Multiple answers are possible.')}</div> : null
  const questionHelpText = props.question.help_text ? <div className="poll__help-text">{props.question.help_text}</div> : null
  const [userChoices, setUserChoices] = useState(props.question.userChoices)
  const [otherChoiceAnswer, setOtherChoiceAnswer] = useState(getUserAnswer())

  const handleSingleChange = (event) => {
    const choiceId = parseInt(event.target.value)
    setUserChoices([choiceId])
    props.onSingleChange(props.question.id, choiceId)
  }

  const handleMultiChange = (event) => {
    const choiceId = parseInt(event.target.value)
    setUserChoices(prevState => [...prevState, choiceId])
    props.onMultiChange(props.question.id, choiceId)
  }

  const handleOtherChange = (event) => {
    const otherAnswer = event.target.value
    setOtherChoiceAnswer(otherAnswer)
    props.onOtherChange(props.question.id, otherAnswer)
  }

  useEffect(() => setUserChoices(props.question.userChoices))

  return (
    <form>
      <div className="poll">
        <h2>{props.question.label}</h2>
        {questionHelpText}
        {multiHelpText}
        <div className="poll__rows">
          {
            props.question.choices.map((choice, i) => {
              const checked = userChoices.indexOf(choice.id) !== -1

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
                      onChange={(event) => { handleSingleChange(event) }}
                      disabled={!props.question.authenticated}
                    />
                    <span className="radio__text">{choice.label}</span>
                    {choice.is_other_choice &&
                      <input
                        className="input-group__input"
                        type="text"
                        name="question"
                        value={otherChoiceAnswer}
                        id={'id_choice-' + choice.id + '-single-answer'}
                        onChange={(event) => { handleOtherChange(event) }}
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
                      onChange={(event) => { handleMultiChange(event) }}
                      disabled={!props.question.authenticated}
                    />
                    <span className="radio__text radio__text--checkbox">{choice.label}</span>
                    {choice.is_other_choice &&
                      <input
                        className="input-group__input"
                        type="text"
                        name="question"
                        id={'id_choice-' + choice.id + '-single'}
                        value={otherChoiceAnswer}
                        onChange={(event) => { handleOtherChange(event) }}
                        disabled={!props.question.authenticated}
                      />}
                  </label>
                )
              }
            })
          }
        </div>
      </div>
    </form>
  )
}
