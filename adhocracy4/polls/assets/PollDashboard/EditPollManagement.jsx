import React, { useState, useEffect } from 'react'
import django from 'django'
import dashboard from '../../../../adhocracy4/dashboard/assets/dashboard'
import update from 'immutability-helper'
import { EditPollQuestion } from './EditPollQuestion'
import { EditPollOpenQuestion } from './EditPollOpenQuestion'
import Alert from '../../../static/Alert'
import EditPollDropdown from './EditPollDropdown'

const api = require('adhocracy4').api
const FlipMove = require('react-flip-move').default

/*
|--------------------------------------------------------------------------
| Helper method for local scoped key/identifier
|--------------------------------------------------------------------------
*/

let maxLocalKey = 0
const getNextLocalKey = () => {
  /** Get an artificial key for non-committed items.
   *
   *  The key is prefixed to prevent collisions with real database keys.
   */
  return 'local_' + maxLocalKey++
}

export const EditPollManagement = (props) => {
  /*
  |--------------------------------------------------------------------------
  | Question state related handlers
  |--------------------------------------------------------------------------
  */

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

  const getNewOpenQuestion = (label = '') => {
    const newQuestion = getNewQuestion(label)
    newQuestion.is_open = true
    newQuestion.choices = []
    return newQuestion
  }

  const handleQuestion = (action, params) => {
    let diff = {}
    if (action === 'label') {
      const { index, label } = params
      diff[index] = { $merge: { label } }
    } else if (action === 'helptext') {
      const { index, helptext } = params
      diff[index] = { $merge: { help_text: helptext } }
    } else if (action === 'multiple-choice') {
      const { index, multipleChoice } = params
      diff[index] = { $merge: { multiple_choice: multipleChoice } }
    } else if (action === 'move') {
      const { index, direction } = params
      const position = direction === 'up' ? (index - 1) : (index + 1)
      diff = { $splice: [[index, 1], [position, 0, questions[index]]] }
    } else if (action === 'append') {
      const newQuestion = params && params.isOpen
        ? getNewOpenQuestion()
        : getNewQuestion()
      diff = { $push: [newQuestion] }
    } else if (action === 'delete') {
      const { index } = params
      diff = { $splice: [[index, 1]] }
    } else {
      return null
    }
    action && setQuestions(update(questions, diff))
  }

  /*
  |--------------------------------------------------------------------------
  | Choice state related handlers
  |--------------------------------------------------------------------------
  */

  const getNewChoice = (label = '', isOther = false) => {
    return {
      label,
      key: isOther ? 'other-choice' : getNextLocalKey(),
      is_other_choice: isOther
    }
  }

  const handleChoiceLabel = (params) => {
    const diff = {}
    const { index, choiceIndex, label } = params
    diff[index] = { choices: {} }
    diff[index].choices[choiceIndex] = { $merge: { label } }
    setQuestions(update(questions, diff))
  }

  const handleChoiceAppend = (params) => {
    const diff = {}
    const { index, hasOtherOption } = params
    const position = questions[index].choices.length - 1
    const newChoice = getNewChoice()
    diff[index] = hasOtherOption
      ? { choices: { $splice: [[position, 0, newChoice]] } }
      : { choices: { $push: [newChoice] } }
    setQuestions(update(questions, diff))
  }

  const handleChoiceIsOtherChoice = (params) => {
    const diff = {}
    const { index, isOtherChoice } = params
    if (isOtherChoice) {
      const otherChoice = getNewChoice('other', true)
      diff[index] = { choices: { $push: [otherChoice] } }
    } else {
      const choiceIndex = questions[index].choices.findIndex(c => c.key === 'other-choice')
      diff[index] = { choices: { $splice: [[choiceIndex, 1]] } }
    }
    setQuestions(update(questions, diff))
  }

  const handleChoiceDelete = (params) => {
    const diff = {}
    const { index, choiceIndex } = params
    diff[index] = { choices: { $splice: [[choiceIndex, 1]] } }
    setQuestions(update(questions, diff))
  }

  /*
  |--------------------------------------------------------------------------
  | Poll form and submit logic
  |--------------------------------------------------------------------------
  */

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
          type: 'success',
          message: django.gettext('The poll has been updated.')
        })
        setErrors([])
        if (props.reloadOnSuccess) {
          dashboard.updateDashboard()
        }
      })
      .fail((xhr, status, err) => {
        if (xhr.responseJSON && 'questions' in xhr.responseJSON) {
          setErrors(xhr.responseJSON.questions)
        }

        setAlert({
          type: 'danger',
          message: django.gettext('The poll could not be updated.')
        })
      })
  }

  /*
  |--------------------------------------------------------------------------
  | Runtime logic and JSX render
  |--------------------------------------------------------------------------
  */

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
                    onLabelChange={(label) => handleQuestion('label', { index, label })}
                    onHelptextChange={(helptext) => handleQuestion('helptext', { index, helptext })}
                    onMoveUp={index !== 0 ? () => handleQuestion('move', { index, direction: 'up' }) : null}
                    onMoveDown={index < arr.length - 1 ? () => handleQuestion('move', { index, direction: 'down' }) : null}
                    onDelete={() => handleQuestion('delete', { index })}
                    errors={errors && errors[index] ? errors[index] : {}}
                  />
                </div>
                )
              : (
                <div key={key}>
                  <EditPollQuestion
                    id={key}
                    question={question}
                    onLabelChange={(label) => handleQuestion('label', { index, label })}
                    onHelptextChange={(helptext) => handleQuestion('helptext', { index, helptext })}
                    onMultipleChoiceChange={(multipleChoice) => handleQuestion('multiple-choice', { index, multipleChoice })}
                    onHasOtherChoiceChange={(isOtherChoice) => handleChoiceIsOtherChoice(index, isOtherChoice)}
                    onMoveUp={index !== 0 ? () => handleQuestion('move', { index, direction: 'up' }) : null}
                    onMoveDown={index < arr.length - 1 ? () => handleQuestion('move', { index, direction: 'down' }) : null}
                    onDelete={() => handleQuestion('delete', { index })}
                    errors={errors && errors[index] ? errors[index] : {}}
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
      <div className="editpoll__actions-container">
        <div className="editpoll__menu-container">
          <EditPollDropdown
            handleToggleMulti={() => handleQuestion('append')}
            handleToggleOpen={() => handleQuestion('append', { isOpen: true })}
          />
        </div>

        <div className="editpoll__menu-container">
          <button type="submit" className="btn poll__btn--dark">
            {django.gettext('Save')}
          </button>
        </div>
      </div>
    </form>
  )
}
