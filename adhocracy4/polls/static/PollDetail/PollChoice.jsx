import React, { useEffect, useState } from 'react'
import django from 'django'
import { ChoiceRow } from './ChoiceRow'

const translated = {
  multiple: django.gettext('Multiple answers are possible.')
}

export const PollChoice = (props) => {
  const getUserAnswer = () => {
    const userAnswerId = props.question.other_choice_user_answer
    const userAnswer = props.question.other_choice_answers.find(oc => oc.vote_id === userAnswerId)
    return props.question.other_choice_answer
      ? props.question.other_choice_answer
      : ((userAnswerId && userAnswer)
          ? userAnswer.answer
          : ''
        )
  }

  const [userChoices, setUserChoices] = useState([])
  const [otherChoiceAnswer, setOtherChoiceAnswer] = useState(getUserAnswer())
  const [errors, setErrors] = useState()

  const multiHelpText = props.question.multiple_choice ? <div className="poll__help-text">{translated.multiple}</div> : null
  const questionHelpText = props.question.help_text ? <div className="poll__help-text">{props.question.help_text}</div> : null
  const userAllowedVote = props.question.authenticated || props.allowUnregisteredUsers

  useEffect(() => {
    setUserChoices(props.question.userChoices || [])
    setErrors(props.errors)
  }, [props.question.userChoices, props.errors])

  const findOtherChoice = () => {
    return props.question.choices.find(c => c.is_other_choice)
  }

  const handleSingleChange = (event, isOther) => {
    const choiceId = parseInt(event.target.value)
    setUserChoices([choiceId])
    props.onSingleChange(props.question.id, choiceId)
    if (!isOther) {
      setOtherChoiceAnswer('')
      props.onOtherChange(props.question.id, '', findOtherChoice())
    }
  }

  const handleMultiChange = (event, isOther) => {
    const choiceId = parseInt(event.target.value)
    const newChoices = userChoices.includes(choiceId)
      ? userChoices.filter(id => id !== choiceId)
      : [...userChoices, choiceId]

    setUserChoices(newChoices)
    props.onMultiChange(props.question.id, choiceId)

    if (!newChoices.includes(findOtherChoice()?.id)) {
      setOtherChoiceAnswer('')
      props.onOtherChange(props.question.id, '', findOtherChoice())
    }
  }

  const handleOtherChange = (event) => {
    const otherAnswer = event.target.value
    setOtherChoiceAnswer(otherAnswer)
    props.onOtherChange(props.question.id, otherAnswer)
  }

  return (
    <div className="poll poll--question">
      <h3>{props.question.label}</h3>
      {questionHelpText}
      {multiHelpText}
      <div className="poll__rows">
        {props.question.choices.map((choice) => {
          const checked = userChoices.indexOf(choice.id) !== -1
          return (
            <ChoiceRow
              key={choice.id}
              choice={choice}
              checked={checked}
              onInputChange={props.question.multiple_choice ? handleMultiChange : handleSingleChange}
              type={props.question.multiple_choice ? 'checkbox' : 'radio'}
              disabled={!userAllowedVote || props.question.isReadOnly}
              otherChoiceAnswer={otherChoiceAnswer}
              onOtherChange={handleOtherChange}
              isReadOnly={props.question.isReadOnly}
              errors={errors}
            />
          )
        })}
      </div>
    </div>
  )
}
