import React, { useState } from 'react'
import django from 'django'
import dashboard from 'adhocracy4/adhocracy4/dashboard/assets/dashboard'
import update from 'immutability-helper'
import QuestionForm from './QuestionForm'
import Alert from '../../contrib/assets/Alert'
import { PopperMenu } from './PopperMenu'

const api = require('adhocracy4').api
const FlipMove = require('react-flip-move').default

export const PollManagement = (props) => {
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
    maxLocalKey++
    return 'local_' + maxLocalKey
  }

  /*
  |--------------------------------------------------------------------------
  | Question state related handlers
  |--------------------------------------------------------------------------
  */

  const getNewQuestion = (label = '') => {
    return {
      label: label,
      multiple_choice: false,
      key: getNextLocalKey(),
      choices: [
        getNewChoice(),
        getNewChoice()
      ]
    }
  }

  const handleQuestion = (action, params) => {
    let diff = {}
    if (action === 'label') {
      const { index, label } = params
      diff[index] = { $merge: { label: label } }
    } else if (action === 'multiple-choice') {
      const { index, multipleChoice } = params
      diff[index] = { $merge: { multiple_choice: multipleChoice } }
    } else if (action === 'move') {
      const { index, direction } = params
      const position = direction === 'up' ? (index - 1) : (index + 1)
      diff = { $splice: [[index, 1], [position, 0, questions[index]]] }
    } else if (action === 'append') {
      const newQuestion = getNewQuestion()
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

  const getNewChoice = (label = '') => {
    return {
      label: label,
      key: getNextLocalKey()
    }
  }

  const handleChoice = (action, params) => {
    const diff = {}
    if (action === 'label') {
      const { index, choiceIndex, label } = params
      diff[index] = { choices: {} }
      diff[index].choices[choiceIndex] = { $merge: { label: label } }
    } else if (action === 'append') {
      const { index } = params
      const newChoice = getNewChoice()
      diff[index] = { choices: { $push: [newChoice] } }
    } else if (action === 'delete') {
      const { index, choiceIndex } = params
      diff[index] = { choices: { $splice: [[choiceIndex, 1]] } }
    }
    action && setQuestions(update(questions, diff))
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
      questions: questions
    }

    api.poll.change(data, props.poll.id)
      .done((data) => {
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
        setErrors(errors)
      })
  }

  /*
  |--------------------------------------------------------------------------
  | Runtime logic and JSX render
  |--------------------------------------------------------------------------
  */

  const [questions, setQuestions] = useState(props.poll.questions)
  const [errors, setErrors] = useState([])
  const [alert, setAlert] = useState(null)

  questions.length > 0 || (setQuestions([getNewQuestion()]))

  const popperMenuContent = {
    popperButton: {
      styleClass: 'btn btn--light btn--small',
      buttonText: django.gettext('Add a new question'),
      icon: 'fa fa-plus'
    },
    popperMenuItems: [
      {
        styleClass: 'btn btn--light btn--small',
        text: 'vorgegebene Antworten',
        handleClick: () => handleQuestion('append')
      },
      {
        styleClass: 'btn btn--light btn--small',
        text: 'offene Antworten',
        handleClick: () => handleQuestion('append')
      }
    ]
  }

  return (
    <form onSubmit={(e) => handleSubmit(e)} onChange={() => removeAlert()}>
      <FlipMove easing="cubic-bezier(0.25, 0.5, 0.75, 1)">
        {
          questions.map((question, index, arr) => {
            const key = question.id || question.key
            return (
              <div key={key}>
                <QuestionForm
                  id={key}
                  question={question}
                  onLabelChange={(label) => handleQuestion('label', { index, label })}
                  onMultipleChoiceChange={(multipleChoice) => handleQuestion('multiple-choice', index, multipleChoice)}
                  onMoveUp={index !== 0 ? () => handleQuestion('move', { index, direction: 'up' }) : null}
                  onMoveDown={index < arr.length - 1 ? () => handleQuestion('move', { index, direction: 'down' }) : null}
                  onDelete={() => handleQuestion('delete', { index })}
                  errors={errors && errors[index] ? errors[index] : {}}
                  onChoiceLabelChange={(choiceIndex, label) => handleChoice('label', { index, choiceIndex, label })}
                  onDeleteChoice={(choiceIndex) => handleChoice('delete', { index, choiceIndex })}
                  onAppendChoice={() => handleChoice('append', { index })}
                />
              </div>
            )
          })
        }
      </FlipMove>
      <div className="pollmanagement-actions-container">
        <PopperMenu>
          {popperMenuContent}
        </PopperMenu>
        <Alert onClick={() => removeAlert()} {...alert} />
        <button type="submit" className="btn btn--primary">
          {django.gettext('Save')}
        </button>
      </div>
    </form>
  )
}
