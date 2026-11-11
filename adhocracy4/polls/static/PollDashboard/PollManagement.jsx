import React, { useEffect, useRef, useState } from 'react'
import django from 'django'

import api from '../../../static/api'
import Alert from '../../../static/Alert'
import { updateDashboard } from '../../../../adhocracy4/dashboard/assets/dashboard'

import { AddQuestionDropdown } from './AddQuestionDropdown'
import { QuestionEditor } from './QuestionEditor'
import { QuestionListItem } from './QuestionListItem'
import {
  buildQuestionsPayload,
  createEmptyChoice,
  createEmptyQuestion,
  moveItem,
  normalizeQuestion
} from './utils'

const TRANSLATED = {
  optionsTitle: django.gettext('Options'),
  allowUnregisteredUsersLabel: django.gettext('Allow unregistered users to vote'),
  allowUnregisteredUsersSR: django.gettext('Enable this option to allow users who are not registered to participate in the voting process.'),
  hideResultsUntilFinishedLabel: django.gettext('Hide results until participation is over'),
  hideResultsUntilFinishedSR: django.gettext('Enable this option to hide the poll results from participants until the participation phase has ended.'),
  questionsTitle: django.gettext('Questions'),
  addQuestion: django.gettext('New question'),
  save: django.gettext('Save'),
  updated: django.gettext('The poll has been updated.'),
  updateFailed: django.gettext('The poll could not be updated. Please check the data you entered again.'),
  updateFailedStatus: django.gettext('The poll could not be updated (HTTP %(status)s). Please try again.'),
  unsavedChanges: django.gettext('If you leave this page changes you made will not be saved.'),
  loadFailed: django.gettext('The poll could not be loaded. Please try again.'),
  retry: django.gettext('Retry')
}

const hasQuestionErrors = (errors) => {
  if (!errors) return false
  return Object.entries(errors).some(([field, value]) => {
    if (field === 'choices') {
      return Array.isArray(value) && value.some((choice) => (
        choice && Object.values(choice).some((entry) => (
          Array.isArray(entry) ? entry.length > 0 : Boolean(entry)
        ))
      ))
    }
    return Array.isArray(value) ? value.length > 0 : Boolean(value)
  })
}

const collectErrorMessages = (questionErrors) => {
  const messages = []
  questionErrors.forEach((questionError) => {
    if (!questionError) return
    Object.values(questionError).forEach((value) => {
      if (!value) return
      if (Array.isArray(value)) {
        value.forEach((entry) => {
          if (typeof entry === 'string' && entry) {
            messages.push(entry)
          } else if (entry && typeof entry === 'object') {
            Object.values(entry).forEach((nested) => {
              if (Array.isArray(nested) && nested[0]) {
                messages.push(String(nested[0]))
              }
            })
          }
        })
      } else if (typeof value === 'string') {
        messages.push(value)
      }
    })
  })
  return messages.filter((message, index) => messages.indexOf(message) === index)
}

export const PollManagement = (props) => {
  const [questions, setQuestions] = useState([])
  const [allowUnregisteredUsers, setAllowUnregisteredUsers] = useState(false)
  const [hideResultsUntilFinished, setHideResultsUntilFinished] = useState(false)
  const [errors, setErrors] = useState([])
  const [alert, setAlert] = useState(null)
  const [expandedKey, setExpandedKey] = useState(null)
  const [dragIndex, setDragIndex] = useState(null)
  const [overIndex, setOverIndex] = useState(null)
  const [dirty, setDirty] = useState(false)
  const [loaded, setLoaded] = useState(false)
  const [loadFailed, setLoadFailed] = useState(false)
  const [loadAttempt, setLoadAttempt] = useState(0)
  const focusErrorRef = useRef(false)
  const scrollToEditorRef = useRef(false)
  const touchDragIndexRef = useRef(null)
  // Bumped on every edit so a late save response cannot overwrite newer edits.
  const editRevisionRef = useRef(0)

  useEffect(() => {
    setLoaded(false)
    setLoadFailed(false)
    api.poll.get(props.pollId).done((result) => {
      const initialQuestions = result.questions.length
        ? result.questions.map(normalizeQuestion)
        : [createEmptyQuestion(false)]
      setQuestions(initialQuestions)
      setAllowUnregisteredUsers(result.allow_unregistered_users)
      setHideResultsUntilFinished(result.hide_results_until_finished)
      setLoaded(true)
      setAlert(null)
    }).fail(() => {
      setLoadFailed(true)
      setAlert({ type: 'danger', message: TRANSLATED.loadFailed })
    })
  }, [props.pollId, loadAttempt])

  const expandedIndex = questions.findIndex((question) => question.key === expandedKey)

  // Native unsaved-changes warning. The global unload_warning.js only arms on
  // native "change" events, so button-only edits (answer type, add/delete,
  // reorder) would not be covered. Track a dirty flag for every edit.
  useEffect(() => {
    if (!dirty) return undefined
    const handler = (event) => {
      event.preventDefault()
      event.returnValue = TRANSLATED.unsavedChanges
      return TRANSLATED.unsavedChanges
    }
    window.addEventListener('beforeunload', handler)
    return () => window.removeEventListener('beforeunload', handler)
  }, [dirty])

  // Move focus (and the viewport) to the first invalid field after a failed save.
  useEffect(() => {
    if (!focusErrorRef.current || !expandedKey) return
    const field = document.querySelector('.poll-management__editor [aria-invalid="true"]')
    if (field) {
      field.focus()
      field.scrollIntoView?.({ block: 'center' })
    }
    focusErrorRef.current = false
  }, [errors, expandedKey, questions])

  // Keep the edited question in view after a successful save.
  useEffect(() => {
    if (!scrollToEditorRef.current || !expandedKey) return
    const editor = document.querySelector('.poll-management__editor')
    editor?.scrollIntoView?.({ block: 'start', behavior: 'smooth' })
    scrollToEditorRef.current = false
  }, [expandedKey, questions])

  const markDirty = () => {
    editRevisionRef.current += 1
    setDirty(true)
  }

  const updateQuestion = (index, updates) => {
    setQuestions((prev) => prev.map((question, i) => (
      i === index ? { ...question, ...updates } : question
    )))
    markDirty()
    // Only clear the errors of the fields that were actually edited, so the
    // remaining invalid fields stay marked until they are fixed as well.
    setErrors((prev) => {
      const questionError = prev[index]
      if (!questionError) return prev
      const fields = Object.keys(updates)
      if (!fields.some((field) => field in questionError)) return prev
      const next = [...prev]
      const cleared = { ...questionError }
      fields.forEach((field) => { delete cleared[field] })
      next[index] = cleared
      return next
    })
  }

  const updateChoice = (questionIndex, choiceIndex, updates) => {
    setQuestions((prev) => prev.map((question, i) => {
      if (i !== questionIndex) return question
      return {
        ...question,
        choices: question.choices.map((choice, j) => (
          j === choiceIndex ? { ...choice, ...updates } : choice
        ))
      }
    }))
    markDirty()
    setErrors((prev) => {
      const questionError = prev[questionIndex]
      const choiceErrors = questionError?.choices
      if (!questionError || !Array.isArray(choiceErrors)) return prev
      const current = choiceErrors[choiceIndex]
      if (!current) return prev
      const fields = Object.keys(updates)
      if (!fields.some((field) => field in current)) return prev
      const next = [...prev]
      const nextChoices = [...choiceErrors]
      const cleared = { ...current }
      fields.forEach((field) => { delete cleared[field] })
      nextChoices[choiceIndex] = cleared
      next[questionIndex] = { ...questionError, choices: nextChoices }
      return next
    })
  }

  const clearAlert = () => {
    setAlert(null)
  }

  const handleEdit = (key) => {
    // clicking the row again collapses it, keeping the local edits
    if (key === expandedKey) {
      setExpandedKey(null)
      return
    }
    if (questions.some((item) => item.key === key)) {
      setExpandedKey(key)
    }
  }

  // The up/down controls change the position of the current question within
  // the survey instead of navigating to a different question.
  const handleMove = (direction) => {
    const newIndex = expandedIndex + direction
    if (expandedIndex < 0 || newIndex < 0 || newIndex >= questions.length) return
    setQuestions((prev) => moveItem(prev, expandedIndex, newIndex))
    markDirty()
    setErrors([])
  }

  const handleQuestionAppend = (isOpen, multipleChoice = false) => {
    const question = createEmptyQuestion(isOpen, multipleChoice)
    setQuestions((prev) => [...prev, question])
    setExpandedKey(question.key)
    markDirty()
    setErrors([])
  }

  const handleQuestionDelete = (index) => {
    // The update endpoint ignores an empty question list, so the editor always
    // keeps at least one question to avoid a save that silently does nothing.
    if (questions.length <= 1) return
    if (questions[index].key === expandedKey) {
      setExpandedKey(null)
    }
    setQuestions((prev) => prev.filter((_, i) => i !== index))
    markDirty()
    setErrors([])
  }

  // Switching a question to/from the open (free text) type also adjusts the
  // choices: open questions have none, choice questions need at least two.
  const handleOpenChange = (isOpen) => {
    setQuestions((prev) => prev.map((question, i) => {
      if (i !== expandedIndex || question.is_open === isOpen) return question
      if (isOpen) {
        return { ...question, is_open: true, choices: [] }
      }
      return {
        ...question,
        is_open: false,
        choices: question.choices.length
          ? question.choices
          : [createEmptyChoice(), createEmptyChoice()]
      }
    }))
    markDirty()
  }

  const handleAnswerTypeChange = (multipleChoice) => {
    updateQuestion(expandedIndex, { multiple_choice: multipleChoice })
  }

  const handleDragStart = (index) => setDragIndex(index)

  const handleDragEnter = (index) => {
    if (dragIndex !== null && index !== overIndex) {
      setOverIndex(index)
    }
  }

  const handleDrop = () => {
    if (dragIndex !== null && overIndex !== null) {
      setQuestions((prev) => moveItem(prev, dragIndex, overIndex))
      markDirty()
      setErrors([])
    }
    handleDragEnd()
  }

  const handleDragEnd = () => {
    setDragIndex(null)
    setOverIndex(null)
  }

  // Touch/pen devices do not support native HTML5 drag and drop, so reordering
  // via the drag handle needs a Pointer Events fallback (mouse keeps using the
  // native drag events above).
  const itemIndexFromPoint = (x, y) => {
    const element = document.elementFromPoint(x, y)
    const item = element?.closest('.poll-management__list-item')
    if (!item || !item.parentElement) return null
    const index = Array.from(item.parentElement.children).indexOf(item)
    return index >= 0 ? index : null
  }

  const handleListPointerDown = (e) => {
    if (e.pointerType === 'mouse') return
    const target = e.target
    if (!target.closest('.poll-management__drag-handle')) return
    const index = itemIndexFromPoint(e.clientX, e.clientY)
    if (index === null) return
    try {
      e.currentTarget.setPointerCapture(e.pointerId)
    } catch {
      // capture is best-effort; dragging still works while over the list
    }
    touchDragIndexRef.current = index
    setDragIndex(index)
    setOverIndex(index)
  }

  const handleListPointerMove = (e) => {
    if (touchDragIndexRef.current === null) return
    const index = itemIndexFromPoint(e.clientX, e.clientY)
    if (index !== null && index !== overIndex) {
      setOverIndex(index)
    }
  }

  const handleListPointerUp = (e) => {
    if (touchDragIndexRef.current === null) return
    try {
      if (e.currentTarget.hasPointerCapture(e.pointerId)) {
        e.currentTarget.releasePointerCapture(e.pointerId)
      }
    } catch {
      // ignore missing capture
    }
    touchDragIndexRef.current = null
    handleDrop()
  }

  // A canceled gesture must not move a question, so release the capture and
  // reset the drag state without calling handleDrop.
  const handleListPointerCancel = (e) => {
    if (touchDragIndexRef.current === null) return
    try {
      if (e.currentTarget.hasPointerCapture(e.pointerId)) {
        e.currentTarget.releasePointerCapture(e.pointerId)
      }
    } catch {
      // ignore missing capture
    }
    touchDragIndexRef.current = null
    handleDragEnd()
  }

  const handleChoiceLabelChange = (choiceIndex, label) => {
    updateChoice(expandedIndex, choiceIndex, { label })
  }

  const handleChoiceDelete = (choiceIndex) => {
    setQuestions((prev) => prev.map((question, i) => {
      if (i !== expandedIndex) return question
      return {
        ...question,
        choices: question.choices.filter((_, j) => j !== choiceIndex)
      }
    }))
    markDirty()
  }

  const handleChoiceAppend = () => {
    setQuestions((prev) => prev.map((question, i) => {
      if (i !== expandedIndex) return question
      const hasOtherOption = question.choices.some((choice) => choice.is_other_choice)
      const position = hasOtherOption ? question.choices.length - 1 : question.choices.length
      const choices = [...question.choices]
      choices.splice(position, 0, createEmptyChoice())
      return { ...question, choices }
    }))
    markDirty()
  }

  const handleOtherChoiceToggle = () => {
    setQuestions((prev) => prev.map((question, i) => {
      if (i !== expandedIndex) return question
      const hasOtherOption = question.choices.some((choice) => choice.is_other_choice)
      if (hasOtherOption) {
        return {
          ...question,
          choices: question.choices.filter((choice) => !choice.is_other_choice)
        }
      }
      return { ...question, choices: [...question.choices, createEmptyChoice(true)] }
    }))
    markDirty()
  }

  const handleImageChange = (questionKey, base64) => {
    const index = questions.findIndex((question) => question.key === questionKey)
    if (index === -1) return
    updateQuestion(index, {
      image_base64: base64 || '',
      image_url: base64 || null,
      image_alt_text: ''
    })
  }

  const handleAltTextChange = (altText) => {
    updateQuestion(expandedIndex, { image_alt_text: altText })
  }

  const handleSubmit = (e) => {
    e.preventDefault()

    const payload = {
      questions: buildQuestionsPayload(questions),
      allow_unregistered_users: allowUnregisteredUsers,
      hide_results_until_finished: hideResultsUntilFinished
    }
    const submitExpandedIndex = expandedIndex
    const submittedRevision = editRevisionRef.current

    api.poll.change(payload, props.pollId)
      .done((response) => {
        setAlert({ type: 'success', message: TRANSLATED.updated })
        if (props.reloadOnSuccess) updateDashboard()
        // Ignore a response that arrives after further edits: the local state
        // is newer than the saved poll, so it must stay untouched and dirty.
        if (editRevisionRef.current !== submittedRevision) return
        const normalized = response.questions.map((question) => ({
          ...normalizeQuestion(question),
          image_base64: null
        }))
        setQuestions(normalized)
        setErrors([])
        // Keep the question that was being edited open and bring it back into
        // view instead of collapsing everything and jumping to the top.
        const savedQuestion = submitExpandedIndex >= 0 ? normalized[submitExpandedIndex] : undefined
        if (savedQuestion) {
          setExpandedKey(savedQuestion.key)
          scrollToEditorRef.current = true
        } else {
          setExpandedKey(null)
        }
        setDirty(false)
      })
      .fail((xhr) => {
        let questionErrors = []
        let messages = []
        let parsed = null
        try {
          parsed = xhr && xhr.responseText ? JSON.parse(xhr.responseText) : null
        } catch {
          // response body was not valid JSON (e.g. a proxy or server error page)
        }
        if (parsed && Array.isArray(parsed.questions)) {
          questionErrors = parsed.questions
          messages = collectErrorMessages(questionErrors)
        } else if (parsed) {
          messages = collectErrorMessages([parsed])
        }
        setErrors(questionErrors)
        const firstErrorIndex = questionErrors.findIndex(hasQuestionErrors)
        if (firstErrorIndex !== -1 && questions[firstErrorIndex]) {
          setExpandedKey(questions[firstErrorIndex].key)
          focusErrorRef.current = true
        }
        const status = xhr && xhr.status
        let message = messages.join(' ')
        if (!message) {
          message = status
            ? django.interpolate(TRANSLATED.updateFailedStatus, { status }, true)
            : TRANSLATED.updateFailed
        }
        setAlert({ type: 'danger', message })
      })
  }

  if (loadFailed) {
    return (
      <div className="poll-management">
        <Alert type="danger" message={TRANSLATED.loadFailed} />
        <button
          type="button"
          className="btn btn--primary"
          onClick={() => setLoadAttempt((attempt) => attempt + 1)}
        >
          {TRANSLATED.retry}
        </button>
      </div>
    )
  }

  // Do not offer the editor before the questions were loaded: an empty editor
  // would submit an empty question list.
  if (!loaded) return null

  return (
    <form className="poll-management" onSubmit={handleSubmit}>
      <section className="poll-management__questions">
        <div className="poll-management__questions-header">
          <h2 className="poll-management__section-title">{TRANSLATED.questionsTitle}</h2>
          <AddQuestionDropdown
            onAddMultipleChoice={() => handleQuestionAppend(false, true)}
            onAddOpen={() => handleQuestionAppend(true)}
          />
        </div>

        <ul
          className="poll-management__list"
          onPointerDown={handleListPointerDown}
          onPointerMove={handleListPointerMove}
          onPointerUp={handleListPointerUp}
          onPointerCancel={handleListPointerCancel}
        >
          {questions.map((question, index) => (
            <li key={question.key} className="poll-management__list-item">
              <QuestionListItem
                question={question}
                index={index}
                hasErrors={hasQuestionErrors(errors[index])}
                isExpanded={question.key === expandedKey}
                isDragging={dragIndex === index}
                isDragOver={overIndex === index && dragIndex !== null && dragIndex !== index}
                onEdit={() => handleEdit(question.key)}
                onDelete={() => handleQuestionDelete(index)}
                onDragStart={() => handleDragStart(index)}
                onDragEnter={() => handleDragEnter(index)}
                onDragEnd={handleDragEnd}
                onDrop={handleDrop}
              />
              {question.key === expandedKey && (
                <QuestionEditor
                  question={question}
                  index={index}
                  total={questions.length}
                  errors={errors[index] || {}}
                  questionImagesEnabled={Boolean(props.questionImagesEnabled)}
                  onLabelChange={(label) => updateQuestion(index, { label })}
                  onHelpTextChange={(helpText) => updateQuestion(index, { help_text: helpText })}
                  onConfidentialChange={(value) => updateQuestion(index, { is_confidential: value })}
                  onMultipleChoiceChange={handleAnswerTypeChange}
                  onOpenChange={handleOpenChange}
                  onImageChange={handleImageChange}
                  onAltTextChange={handleAltTextChange}
                  onChoiceLabelChange={handleChoiceLabelChange}
                  onChoiceDelete={handleChoiceDelete}
                  onChoiceAppend={handleChoiceAppend}
                  onOtherChoiceToggle={handleOtherChoiceToggle}
                  onMove={handleMove}
                />
              )}
            </li>
          ))}
        </ul>

        <Alert onClick={clearAlert} {...alert} />

        <div className="poll-management__footer">
          <AddQuestionDropdown
            onAddMultipleChoice={() => handleQuestionAppend(false, true)}
            onAddOpen={() => handleQuestionAppend(true)}
          />
          <button type="submit" className="btn btn--primary">
            {TRANSLATED.save}
          </button>
        </div>

        <section className="poll-management__options">
          <h2 className="poll-management__section-title">{TRANSLATED.optionsTitle}</h2>
          {props.enableUnregisteredUsers && (
            <div className="poll-management__option form-check">
              <input
                type="checkbox"
                id="allowUnregisteredUsersCheckbox"
                onChange={() => {
                  setAllowUnregisteredUsers((value) => !value)
                  markDirty()
                }}
                checked={allowUnregisteredUsers}
                aria-describedby="votingDescription"
              />
              <label htmlFor="allowUnregisteredUsersCheckbox">
                {TRANSLATED.allowUnregisteredUsersLabel}
              </label>
              <p id="votingDescription" className="visually-hidden">
                {TRANSLATED.allowUnregisteredUsersSR}
              </p>
            </div>
          )}
          <div className="poll-management__option form-check">
            <input
              type="checkbox"
              id="hideResultsUntilFinishedCheckbox"
              onChange={() => {
                setHideResultsUntilFinished((value) => !value)
                markDirty()
              }}
              checked={hideResultsUntilFinished}
              aria-describedby="hideResultsDescription"
            />
            <label htmlFor="hideResultsUntilFinishedCheckbox">
              {TRANSLATED.hideResultsUntilFinishedLabel}
            </label>
            <p id="hideResultsDescription" className="visually-hidden">
              {TRANSLATED.hideResultsUntilFinishedSR}
            </p>
          </div>
        </section>
      </section>
    </form>
  )
}
