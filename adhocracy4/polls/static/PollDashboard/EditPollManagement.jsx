/* eslint-disable camelcase */
/* eslint-disable no-restricted-syntax */
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

const TRANSLATED = {
  votingOptionsSectionTitle: django.gettext('Voting Options'),
  allowUnregisteredUsersLabel: django.gettext('Allow unregistered users to vote'),
  allowUnregisteredUsersSR: django.gettext('Enable this option to allow users who are not registered to participate in the voting process.'),
  addAndEditSectionTitle: django.gettext('Add and Edit Questions')
}

let maxLocalKey = 0
const getNextLocalKey = () => `local_${maxLocalKey++}`

const createEmptyChoice = (isOther = false) => ({
  label: isOther ? 'other' : '',
  key: isOther ? 'other-choice' : getNextLocalKey(),
  is_other_choice: isOther
})

const createEmptyQuestion = (label = '', helpText = '', isOpen = false) => ({
  label,
  help_text: helpText,
  multiple_choice: false,
  is_confidential: false,
  key: getNextLocalKey(),
  is_open: isOpen,
  choices: isOpen ? [] : [createEmptyChoice(), createEmptyChoice()],
  answers: [],
  image_base64: null,
  image_url: null
})

export const EditPollManagement = (props) => {
  const [questions, setQuestions] = useState([])
  const [allowUnregisteredUsers, setAllowUnregisteredUsers] = useState(false)
  const [errors, setErrors] = useState([])
  const [alert, setAlert] = useState(null)

  useEffect(() => {
    api.poll.get(props.pollId).done(result => {
      const initialQuestions = result.questions.length
        ? result.questions
        : [createEmptyQuestion()]
      setQuestions(initialQuestions)
      setAllowUnregisteredUsers(result.allow_unregistered_users)
    })
  }, [props.pollId])

  const updateQuestion = (index, updates) => {
    setQuestions(update(questions, { [index]: { $merge: updates } }))
  }

  const updateChoice = (qIndex, cIndex, updates) => {
    setQuestions(update(questions, {
      [qIndex]: { choices: { [cIndex]: { $merge: updates } } }
    }))
  }

  const handleQuestionLabel = (index, label) => updateQuestion(index, { label })
  const handleQuestionHelpText = (index, helpText) => updateQuestion(index, { help_text: helpText })
  const handleQuestionMultiChoice = (index, multipleChoice) => updateQuestion(index, { multiple_choice: multipleChoice })
  const handleQuestionConfidential = (index, isConfidential) => updateQuestion(index, { is_confidential: isConfidential })
  const handleQuestionImage = (index, imageBase64) => updateQuestion(index, {
    image_base64: imageBase64 || '',
    image_url: imageBase64 || null
  })

  const handleQuestionAppend = (isOpen = false) => {
    setQuestions([...questions, createEmptyQuestion('', '', isOpen)])
  }

  const handleQuestionDelete = (index) => {
    setQuestions(questions.filter((_, i) => i !== index))
  }

  const handleQuestionMove = (index, direction) => {
    const newIndex = index + direction
    if (newIndex < 0 || newIndex >= questions.length) return

    const reordered = [...questions]
    const temp = reordered[index]
    reordered[index] = reordered[newIndex]
    reordered[newIndex] = temp

    setQuestions(reordered)
  }

  const handleChoiceLabel = (qIndex, cIndex, label) => updateChoice(qIndex, cIndex, { label })
  const handleChoiceDelete = (qIndex, cIndex) => {
    const newChoices = questions[qIndex].choices.filter((_, i) => i !== cIndex)
    updateQuestion(qIndex, { choices: newChoices })
  }

  const handleChoiceAppend = (qIndex, hasOtherOption) => {
    const question = questions[qIndex]
    const position = question.choices.length - 1
    const newChoice = createEmptyChoice()

    setQuestions(update(questions, {
      [qIndex]: hasOtherOption
        ? { choices: { $splice: [[position, 0, newChoice]] } }
        : { choices: { $push: [newChoice] } }
    }))
  }

  const handleChoiceIsOtherChoice = (qIndex, isOtherChoice) => {
    const question = questions[qIndex]
    if (isOtherChoice) {
      setQuestions(update(questions, {
        [qIndex]: { choices: { $push: [createEmptyChoice(true)] } }
      }))
    } else {
      const otherIndex = question.choices.findIndex(c => c.key === 'other-choice')
      if (otherIndex !== -1) {
        const newChoices = question.choices.filter((_, i) => i !== otherIndex)
        updateQuestion(qIndex, { choices: newChoices })
      }
    }
  }

  const clearAlert = () => setAlert(null)

  const handleSubmit = (e) => {
    e.preventDefault()

    const payload = {
      questions: questions.map(q => {
        const { key, answers, imageUrl, image_base64, ...clean } = q
        clean.image_base64 = image_base64 === '' ? '' : (image_base64 || '')
        return clean
      }),
      allow_unregistered_users: allowUnregisteredUsers
    }

    api.poll.change(payload, props.pollId)
      .done(response => {
        setQuestions(response.questions.map(q => ({
          ...q,
          image_base64: null,
          key: q.id || getNextLocalKey()
        })))
        setAlert({ type: 'success', message: django.gettext('The poll has been updated.') })
        setErrors([])
        if (props.reloadOnSuccess) updateDashboard()
      })
      .fail(xhr => {
        try {
          const parsed = JSON.parse(xhr.responseText)
          if (parsed?.questions) {
            setErrors(parsed.questions)
          }
        } catch (e) {
          // console.log('Not JSON, raw HTML:', xhr.responseText.substring(0, 500))
        }
        setAlert({
          type: 'danger',
          message: django.gettext('The poll could not be updated. Please check the data you entered again.')
        })
      })
  }

  return (
    <form onSubmit={handleSubmit} onChange={clearAlert} className="editpoll__questions">
      {props.enableUnregisteredUsers && (
        <section className="editpoll__questions-options">
          <h2>{TRANSLATED.votingOptionsSectionTitle}</h2>
          <div className="editpoll__questions-options__form-check">
            <input
              type="checkbox"
              id="allowUnregisteredUsersCheckbox"
              onChange={() => setAllowUnregisteredUsers(v => !v)}
              checked={allowUnregisteredUsers}
              aria-describedby="votingDescription"
            />
            <label htmlFor="allowUnregisteredUsersCheckbox">
              {TRANSLATED.allowUnregisteredUsersLabel}
            </label>
            <p id="votingDescription" className="a4-sr-only">
              {TRANSLATED.allowUnregisteredUsersSR}
            </p>
          </div>
        </section>
      )}

      <section>
        <h2>{TRANSLATED.addAndEditSectionTitle}</h2>
        <FlipMove easing="cubic-bezier(0.25, 0.5, 0.75, 1)">
          {questions.map((question, index, arr) => {
            const key = question.id || question.key
            const commonProps = {
              id: key,
              key,
              question,
              errors: errors?.[index] || {},
              onLabelChange: (label) => handleQuestionLabel(index, label),
              onHelptextChange: (text) => handleQuestionHelpText(index, text),
              onConfidentialChange: (val) => handleQuestionConfidential(index, val),
              onMoveUp: index > 0 ? () => handleQuestionMove(index, -1) : null,
              onMoveDown: index < arr.length - 1 ? () => handleQuestionMove(index, 1) : null,
              onDelete: () => handleQuestionDelete(index)
            }

            return question.is_open
              ? <EditPollOpenQuestion {...commonProps} onImageChange={(image) => handleQuestionImage(index, image)} />
              : <EditPollQuestion
                  {...commonProps}
                  onMultipleChoiceChange={(val) => handleQuestionMultiChoice(index, val)}
                  onHasOtherChoiceChange={(val) => handleChoiceIsOtherChoice(index, val)}
                  onChoiceLabelChange={(cIndex, label) => handleChoiceLabel(index, cIndex, label)}
                  onDeleteChoice={(cIndex) => handleChoiceDelete(index, cIndex)}
                  onAppendChoice={(hasOther) => handleChoiceAppend(index, hasOther)}
                  onImageChange={(image) => handleQuestionImage(index, image)}
                />
          })}
        </FlipMove>
      </section>

      <Alert onClick={clearAlert} {...alert} />

      <div className="editpoll__question-container">
        <div className="editpoll__question">
          <EditPollDropdown
            handleToggleMulti={() => handleQuestionAppend(false)}
            handleToggleOpen={() => handleQuestionAppend(true)}
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
