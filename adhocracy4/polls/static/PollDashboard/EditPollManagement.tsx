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
import type { PollChoiceEdit, PollEditPayload, PollQuestion, PollQuestionEdit } from '../../../static/api/types'

const TRANSLATED = {
  votingOptionsSectionTitle: django.gettext('Options'),
  allowUnregisteredUsersLabel: django.gettext('Allow unregistered users to vote'),
  allowUnregisteredUsersSR: django.gettext('Enable this option to allow users who are not registered to participate in the voting process.'),
  hideResultsUntilFinishedLabel: django.gettext('Hide results until participation is over'),
  hideResultsUntilFinishedSR: django.gettext('Enable this option to hide the poll results from participants until the participation phase has ended.'),
  addAndEditSectionTitle: django.gettext('Add and Edit Questions')
}

interface EditPollManagementProps {
  pollId: number
  enableUnregisteredUsers: boolean
  reloadOnSuccess: boolean
  questionImagesEnabled: boolean
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
  image_url: null,
  image_alt_text: ''
})

export const EditPollManagement = (props: EditPollManagementProps) => {
  const [questions, setQuestions] = useState<PollQuestionEdit[]>([])
  const [allowUnregisteredUsers, setAllowUnregisteredUsers] = useState(false)
  const [hideResultsUntilFinished, setHideResultsUntilFinished] = useState(false)
  const [errors, setErrors] = useState<Record<string, string[]>[]>([])
  const [alert, setAlert] = useState<{ type: string; message: string } | null>(null)

  useEffect(() => {
    api.poll.get(props.pollId).done(result => {
      const initialQuestions = result.questions.length
        ? result.questions
        : [createEmptyQuestion()]
      setQuestions(initialQuestions)
      setAllowUnregisteredUsers(result.allow_unregistered_users)
      setHideResultsUntilFinished(result.hide_results_until_finished)
    })
  }, [props.pollId])

  const updateQuestion = (index: number, updates: Partial<PollQuestionEdit>) => {
    setQuestions(update(questions, { [index]: { $merge: updates } }))
  }

  const updateChoice = (qIndex: number, cIndex: number, updates: Partial<PollChoiceEdit>) => {
    setQuestions(update(questions, {
      [qIndex]: { choices: { [cIndex]: { $merge: updates } } }
    }))
  }

  const handleQuestionLabel = (index: number, label: string) => updateQuestion(index, { label })
  const handleQuestionHelpText = (index: number, helpText: string) => updateQuestion(index, { help_text: helpText })
  const handleQuestionMultiChoice = (index: number, multipleChoice: boolean) => updateQuestion(index, { multiple_choice: multipleChoice })
  const handleQuestionConfidential = (index: number, isConfidential: boolean) => updateQuestion(index, { is_confidential: isConfidential })
  const handleQuestionImage = (index: number, imageBase64: string | null) => {
    updateQuestion(index, {
      image_base64: imageBase64 || '',
      image_url: imageBase64 || null,
      image_alt_text: ''
    })
    if (!imageBase64) setErrors([])
  }

  const handleQuestionAltText = (index: number, altText: string) => updateQuestion(index, { image_alt_text: altText })

  const handleQuestionAppend = (isOpen = false) => {
    setQuestions([...questions, createEmptyQuestion('', '', isOpen)])
  }

  const handleQuestionDelete = (index: number) => {
    setQuestions(questions.filter((_, i) => i !== index))
  }

  const handleQuestionMove = (index: number, direction: number) => {
    const newIndex = index + direction
    if (newIndex < 0 || newIndex >= questions.length) return

    const reordered = [...questions]
    const temp = reordered[index]
    reordered[index] = reordered[newIndex]
    reordered[newIndex] = temp

    setQuestions(reordered)
  }

  const handleChoiceLabel = (qIndex: number, cIndex: number, label: string) => updateChoice(qIndex, cIndex, { label })
  const handleChoiceDelete = (qIndex: number, cIndex: number) => {
    const newChoices = questions[qIndex].choices.filter((_: PollChoiceEdit, i: number) => i !== cIndex)
    updateQuestion(qIndex, { choices: newChoices })
  }

  const handleChoiceAppend = (qIndex: number, hasOtherOption: boolean) => {
    const question = questions[qIndex]
    const position = question.choices.length - 1
    const newChoice = createEmptyChoice()

    setQuestions(update(questions, {
      [qIndex]: hasOtherOption
        ? { choices: { $splice: [[position, 0, newChoice]] } }
        : { choices: { $push: [newChoice] } }
    }))
  }

  const handleChoiceIsOtherChoice = (qIndex: number, isOtherChoice: boolean) => {
    const question = questions[qIndex]
    if (isOtherChoice) {
      setQuestions(update(questions, {
        [qIndex]: { choices: { $push: [createEmptyChoice(true)] } }
      }))
    } else {
      const otherIndex = question.choices.findIndex((c: PollChoiceEdit) => c.key === 'other-choice')
      if (otherIndex !== -1) {
        const newChoices = question.choices.filter((_: PollChoiceEdit, i: number) => i !== otherIndex)
        updateQuestion(qIndex, { choices: newChoices })
      }
    }
  }

  const clearAlert = () => {
    setAlert(null)
    setErrors([])
  }

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()

    const payload = {
      questions: questions.map(q => {
        const { key: _key, answers: _answers, image_url: _image_url, image_base64, image_alt_text, ...clean } = q
        const cleanPayload: PollEditPayload['questions'][number] = clean

        if (props.questionImagesEnabled) {
          if (image_base64 !== undefined && image_base64 !== null) {
            cleanPayload.image_base64 = image_base64 === '' ? '' : image_base64
          }
          cleanPayload.image_alt_text = image_alt_text || ''
        }

        return cleanPayload
      }),
      allow_unregistered_users: allowUnregisteredUsers,
      hide_results_until_finished: hideResultsUntilFinished
    }

    api.poll.change(payload, props.pollId)
      .done(response => {
        setQuestions(response.questions.map((q: PollQuestion) => ({
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
          const text: string = xhr.responseText
          if (text) {
            const parsed = JSON.parse(text)
            if (parsed?.questions) {
              setErrors(parsed.questions)
            } else {
              console.error('Poll save error (unexpected JSON shape):', parsed)
            }
          } else {
            console.error('Poll save error (no response body)')
          }
        } catch {
          const text: string = xhr.responseText
          console.error('Poll save error (non-JSON response):', text ? text.substring(0, 1000) : 'no response body')
        }
        setAlert({
          type: 'danger',
          message: django.gettext('The poll could not be updated. Please check the data you entered again.')
        })
      })
  }

  return (
    <form onSubmit={handleSubmit} onChange={clearAlert} className="editpoll__questions">
      <section className="editpoll__questions-options">
        <h2>{TRANSLATED.votingOptionsSectionTitle}</h2>
        {props.enableUnregisteredUsers && (
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
        )}
        <div className="editpoll__questions-options__form-check">
          <input
            type="checkbox"
            id="hideResultsUntilFinishedCheckbox"
            onChange={() => setHideResultsUntilFinished(v => !v)}
            checked={hideResultsUntilFinished}
            aria-describedby="hideResultsDescription"
          />
          <label htmlFor="hideResultsUntilFinishedCheckbox">
            {TRANSLATED.hideResultsUntilFinishedLabel}
          </label>
          <p id="hideResultsDescription" className="a4-sr-only">
            {TRANSLATED.hideResultsUntilFinishedSR}
          </p>
        </div>
      </section>

      <section>
        <h2>{TRANSLATED.addAndEditSectionTitle}</h2>
        <FlipMove easing="cubic-bezier(0.25, 0.5, 0.75, 1)">
          {questions.map((question: PollQuestionEdit, index: number, arr: PollQuestionEdit[]) => {
            const key = question.id || question.key || getNextLocalKey()
            const commonProps = {
              id: key,
              key,
              question,
              errors: errors?.[index] || {},
              onLabelChange: (label: string) => handleQuestionLabel(index, label),
              onHelptextChange: (text: string) => handleQuestionHelpText(index, text),
              onConfidentialChange: (val: boolean) => handleQuestionConfidential(index, val),
              onMoveUp: index > 0 ? () => handleQuestionMove(index, -1) : null,
              onMoveDown: index < arr.length - 1 ? () => handleQuestionMove(index, 1) : null,
              onDelete: () => handleQuestionDelete(index)
            }

            return question.is_open
              ? <EditPollOpenQuestion
                  {...commonProps}
                  onImageChange={(image: string | null) => handleQuestionImage(index, image)}
                  onAltTextChange={(text: string) => handleQuestionAltText(index, text)}
                  questionImagesEnabled={props.questionImagesEnabled}
                />
              : <EditPollQuestion
                  {...commonProps}
                  onMultipleChoiceChange={(val: boolean) => handleQuestionMultiChoice(index, val)}
                  onHasOtherChoiceChange={(val: boolean) => handleChoiceIsOtherChoice(index, val)}
                  onChoiceLabelChange={(cIndex: number, label: string) => handleChoiceLabel(index, cIndex, label)}
                  onDeleteChoice={(cIndex: number) => handleChoiceDelete(index, cIndex)}
                  onAppendChoice={(hasOther: boolean) => handleChoiceAppend(index, hasOther)}
                  onImageChange={(image: string | null) => handleQuestionImage(index, image)}
                  onAltTextChange={(text: string) => handleQuestionAltText(index, text)}
                  questionImagesEnabled={props.questionImagesEnabled}
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