import React, { useState, useEffect } from 'react'
import django from 'django'
import FlipMove from 'react-flip-move'
import update from 'immutability-helper'

import { EditPollQuestion } from './EditPollQuestion'
import { EditPollOpenQuestion } from './EditPollOpenQuestion'
import EditPollDropdown from './EditPollDropdown'

import { updateDashboard } from '../../../../adhocracy4/dashboard/assets/dashboard'

import api from '../../../static/api'

import Alert from '../../../static/Alert'

// | Helper method for local scoped key/identifier

let maxLocalKey = 0
const getNextLocalKey = () => {
  // Get an artificial key for non-committed items.
  // The key is prefixed to prevent collisions with real database keys.
  return 'local_' + maxLocalKey++
}

export const EditPollManagement = (props) => {
  const [questions, setQuestions] = useState([])
  const [errors, setErrors] = useState([])
  const [alert, setAlert] = useState(null)

  useEffect(() => {
    api.poll.get(props.pollId).done(({ questions }) => {
      questions.length > 0
        ? setQuestions(questions)
        : setQuestions([getNewQuestion()])
    })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const getNewQuestion = (label = '', helptext = '') => {
    return {
      label,
      help_text: helptext,
      multiple_choice: false,
      key: getNextLocalKey(),
      is_open: false,
      choices: [
        getNewChoice(),
        getNewChoice()
      ],
      answers: []
    }
  }

  // | Question state related handlers

  const getNewOpenQuestion = (label = '') => {
    const newQuestion = getNewQuestion(label)
    newQuestion.is_open = true
    newQuestion.choices = []
    return newQuestion
  }

  const handleQuestionLabel = (index, label) => {
    const diff = {}
    diff[index] = { $merge: { label } }
    setQuestions(update(questions, diff))
  }

  const handleQuestionHelpText = (index, helptext) => {
    const diff = {}
    diff[index] = { $merge: { help_text: helptext } }
    setQuestions(update(questions, diff))
  }

  const handleQuestionMultiChoice = (index, multipleChoice) => {
    const diff = {}
    diff[index] = { $merge: { multiple_choice: multipleChoice } }
    setQuestions(update(questions, diff))
  }

  const handleQuestionAppend = (params, index) => {
    let diff = {}
    const newQuestion = params && params.isOpen
      ? getNewOpenQuestion()
      : getNewQuestion()
    diff = { $push: [newQuestion] }
    setQuestions(update(questions, diff))
  }

  const handleQuestionDelete = (index) => {
    let diff = {}
    diff = { $splice: [[index, 1]] }
    setQuestions(update(questions, diff))
  }

  const handleQuestionMoveUp = (index) => {
    let diff = {}
    const position = index - 1
    diff = {
      $splice: [
        [index, 1], // remove from current index
        [position, 0, questions[index]] // insert to new index
      ]
    }
    setQuestions(update(questions, diff))
  }

  const handleQuestionMoveDown = (index) => {
    let diff = {}
    const position = index + 1
    diff = { $splice: [[index, 1], [position, 0, questions[index]]] }
    setQuestions(update(questions, diff))
  }

  // | Choice state related handlers

  const getNewChoice = (label = '', isOther = false) => {
    return {
      label,
      key: isOther ? 'other-choice' : getNextLocalKey(),
      is_other_choice: isOther
    }
  }

  const handleChoiceLabel = (index, choiceIndex, label) => {
    const diff = {}
    diff[index] = { choices: {} }
    diff[index].choices[choiceIndex] = { $merge: { label } }
    setQuestions(update(questions, diff))
  }

  const handleChoiceAppend = (index, hasOtherOption) => {
    const position = questions[index].choices.length - 1
    const newChoice = getNewChoice()
    const diff = {}
    diff[index] = hasOtherOption
      ? { choices: { $splice: [[position, 0, newChoice]] } }
      : { choices: { $push: [newChoice] } }
    setQuestions(update(questions, diff))
  }

  const handleChoiceIsOtherChoice = (index, isOtherChoice) => {
    const diff = {}
    if (isOtherChoice) {
      const otherChoice = getNewChoice('other', true)
      diff[index] = { choices: { $push: [otherChoice] } }
    } else {
      const choiceIndex = questions[index].choices.findIndex(c => c.key === 'other-choice')
      diff[index] = { choices: { $splice: [[choiceIndex, 1]] } }
    }
    setQuestions(update(questions, diff))
  }

  const handleChoiceDelete = (index, choiceIndex) => {
    const diff = {}
    diff[index] = { choices: { $splice: [[choiceIndex, 1]] } }
    setQuestions(update(questions, diff))
  }

  // | Poll form and submit logic

  const removeAlert = () => {
    setAlert(null)
  }

  const handleSubmit = (e) => {
    e.preventDefault()

    const data = {
      questions
    }

    api.poll.change(data, props.pollId)
      .done((data) => {
        setQuestions(data.questions)
        setAlert({
          alertAttribute: 'polite',
          type: 'success',
          message: django.gettext('The poll has been updated.')
        })
        setErrors([])
        if (props.reloadOnSuccess) {
          updateDashboard()
        }
      })
      .fail((xhr, status, err) => {
        if (xhr.responseJSON && 'questions' in xhr.responseJSON) {
          setErrors(xhr.responseJSON.questions)
        }

        setAlert({
          alertAttribute: 'assertive',
          type: 'danger',
          message: django.gettext(
            'The poll could not be updated. Please check the data you entered again.'
          )
        })
      })
  }

  // | JSX render

  return (
    <form
      onSubmit={(e) => handleSubmit(e)} onChange={() => removeAlert()}
      className="editpoll__questions"
    >
      <FlipMove easing="cubic-bezier(0.25, 0.5, 0.75, 1)">
        {
          questions.map((question, index, arr) => {
            const key = question.id || question.key
            return question.is_open
              ? (
                <div key={key}>
                  <EditPollOpenQuestion
                    id={key}
                    question={question}
                    onLabelChange={(label) => handleQuestionLabel(index, label)}
                    onHelptextChange={(helptext) => handleQuestionHelpText(index, helptext)}
                    onMoveUp={index !== 0 ? () => handleQuestionMoveUp(index) : null}
                    onMoveDown={index < arr.length - 1 ? () => handleQuestionMoveDown(index) : null}
                    onDelete={() => handleQuestionDelete(index)}
                    errors={errors && errors[index] ? errors[index] : {}}
                  />
                </div>
                )
              : (
                <div key={key}>
                  <EditPollQuestion
                    id={key}
                    question={question}
                    onLabelChange={(label) => handleQuestionLabel(index, label)}
                    onHelptextChange={(helptext) => handleQuestionHelpText(index, helptext)}
                    onMultipleChoiceChange={(multipleChoice) => handleQuestionMultiChoice(index, multipleChoice)}
                    onMoveUp={index !== 0 ? () => handleQuestionMoveUp(index) : null}
                    onMoveDown={index < arr.length - 1 ? () => handleQuestionMoveDown(index) : null}
                    onDelete={() => handleQuestionDelete(index)}
                    errors={errors && errors[index] ? errors[index] : {}}
                    onHasOtherChoiceChange={(isOtherChoice) => handleChoiceIsOtherChoice(index, isOtherChoice)}
                    onChoiceLabelChange={(choiceIndex, label) => handleChoiceLabel(index, choiceIndex, label)}
                    onDeleteChoice={(choiceIndex) => handleChoiceDelete(index, choiceIndex)}
                    onAppendChoice={(hasOtherOption) => handleChoiceAppend(index, hasOtherOption)}
                  />
                </div>
                )
          })
        }
      </FlipMove>

      <Alert onClick={() => removeAlert()} {...alert} />

      <div className="editpoll__question-container">
        <div className="editpoll__question">
          <EditPollDropdown
            handleToggleMulti={() => handleQuestionAppend()}
            handleToggleOpen={() => handleQuestionAppend({ isOpen: true })}
          />
        </div>

        <div className="editpoll__question-actions">
          <button type="submit" className="btn btn--primary">
            {django.gettext('Save')}
          </button>
        </div>
      </div>
    </form>
  )
}
