import React, { useEffect, useState } from 'react'
import django from 'django'
import { CharCounter } from './CharCounter'
import FormFieldError from '../../../static/FormFieldError'

const translated = {
  multiple: django.gettext('Multiple answers are possible.'),
  other: django.gettext('other')
}

export const PollQuestion = (props) => {
  // | Function to define state

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

  const [userChoices, setUserChoices] = useState(props.question.userChoices)
  const [otherChoiceAnswer, setOtherChoiceAnswer] = useState(getUserAnswer())
  const [errors, setErrors] = useState()
  const multiHelpText = props.question.multiple_choice ? <div className="poll__help-text">{translated.multiple}</div> : null
  const questionHelpText = props.question.help_text ? <div className="poll__help-text">{props.question.help_text}</div> : null
  const maxlength = 250

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    setUserChoices(props.question.userChoices)
    setErrors(props.errors)
  })

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
    setUserChoices(prevState => [...prevState, choiceId])
    setOtherChoiceAnswer(otherChoiceAnswer)
    props.onMultiChange(props.question.id, choiceId)
    if (isOther) {
      setOtherChoiceAnswer('')
    } else {
      props.onOtherChange(props.question.id, otherChoiceAnswer, findOtherChoice())
    }
  }

  const handleOtherChange = (event) => {
    const otherAnswer = event.target.value
    setOtherChoiceAnswer(otherAnswer)
    props.onOtherChange(props.question.id, otherAnswer)
  }

  const findOtherChoice = () => {
    return props.question.choices.find(c => c.is_other_choice)
  }

  return (
    <form>
      <div className="poll poll--question">
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
                      className="poll-row__radio"
                      type="radio"
                      name="question"
                      id={'id_choice-' + choice.id + '-single'}
                      value={choice.id}
                      checked={checked}
                      onChange={(event) => { handleSingleChange(event, choice.is_other_choice) }}
                      disabled={!props.question.authenticated || props.question.isReadOnly}
                    />
                    <span className="radio__text">{choice.is_other_choice ? translated.other : choice.label}</span>

                    {choice.is_other_choice &&
                      <>
                        <textarea
                          className="form-control"
                          name="question"
                          value={otherChoiceAnswer}
                          id={'id_choice-' + choice.id + '-other'}
                          onChange={(event) => { handleOtherChange(event) }}
                          disabled={!props.question.authenticated || props.question.isReadOnly || !checked}
                          maxLength={maxlength}
                          aria-invalid={props.errors ? 'true' : 'false'}
                          aria-describedby={props.errors && 'id_error-' + props.id}
                        />
                        {checked
                          ? (
                            <>
                              <div className="poll__char-counter">
                                <CharCounter value={otherChoiceAnswer} max={maxlength} />
                              </div>
                              <FormFieldError id={'id_error-' + choice.id} error={errors} field={choice.id} />
                            </>
                            )
                          : null}
                      </>}
                  </label>
                )
              } else {
                return (
                  <label className="poll-row radio" key={choice.id} htmlFor={'id_choice-' + choice.id + '-multiple'}>
                    <input
                      className="poll-row__radio"
                      type="checkbox"
                      name="question"
                      id={'id_choice-' + choice.id + '-multiple'}
                      value={choice.id}
                      checked={checked}
                      onChange={(event) => { handleMultiChange(event, choice.is_other_choice) }}
                      disabled={!props.question.authenticated || props.question.isReadOnly}
                    />
                    <span className="radio__text radio__text--checkbox">{choice.is_other_choice ? translated.other : choice.label}</span>
                    {choice.is_other_choice &&
                      <>
                        <textarea
                          className="form-control"
                          name="question"
                          id={'id_choice-' + choice.id + '-other'}
                          value={otherChoiceAnswer}
                          onChange={(event) => { handleOtherChange(event) }}
                          disabled={!props.question.authenticated || props.question.isReadOnly || !checked}
                          maxLength={maxlength}
                          aria-invalid={props.errors ? 'true' : 'false'}
                          aria-describedby={props.errors && 'id_error-' + props.id}
                        />
                        {checked
                          ? (
                            <>
                              <div className="poll__char-counter">
                                <CharCounter value={otherChoiceAnswer} max={maxlength} />
                              </div>
                              <FormFieldError id={'id_error-' + choice.id} error={errors} field={choice.id} />
                            </>
                            )
                          : null}
                      </>}
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
