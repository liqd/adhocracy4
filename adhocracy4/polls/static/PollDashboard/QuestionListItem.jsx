import React, { useState } from 'react'
import django from 'django'

const TRANSLATED = {
  untitled: django.gettext('Untitled question'),
  multipleChoice: django.gettext('Multiple choice'),
  singleChoice: django.gettext('Single choice'),
  open: django.gettext('Open question'),
  delete: django.gettext('Delete question'),
  confirmDelete: django.gettext('Confirm delete'),
  cancelDelete: django.gettext('Cancel delete'),
  deletePrompt: django.gettext('Delete this question?'),
  expand: django.gettext('Expand question'),
  collapse: django.gettext('Collapse question')
}

const typeLabel = (question) => {
  if (question.is_open) {
    return TRANSLATED.open
  }
  return question.multiple_choice ? TRANSLATED.multipleChoice : TRANSLATED.singleChoice
}

export const QuestionListItem = ({
  question,
  index,
  hasErrors,
  isExpanded,
  isDragging,
  isDragOver,
  onEdit,
  onDelete,
  onDragStart,
  onDragEnter,
  onDragEnd,
  onDrop
}) => {
  const [confirmingDelete, setConfirmingDelete] = useState(false)

  const classNames = [
    'poll-management__item',
    isExpanded ? 'poll-management__item--active' : '',
    isDragging ? 'poll-management__item--dragging' : '',
    isDragOver ? 'poll-management__item--drag-over' : '',
    hasErrors ? 'poll-management__item--error' : ''
  ].filter(Boolean).join(' ')

  return (
    <div
      className={classNames}
      draggable
      onDragStart={(e) => {
        if (e.dataTransfer) {
          e.dataTransfer.effectAllowed = 'move'
          // Firefox only initiates a drag when data is explicitly set
          e.dataTransfer.setData('text/plain', String(index))
        }
        onDragStart()
      }}
      onDragEnter={onDragEnter}
      onDragOver={(e) => {
        e.preventDefault()
        if (e.dataTransfer) {
          e.dataTransfer.dropEffect = 'move'
        }
      }}
      onDrop={(e) => {
        e.preventDefault()
        e.stopPropagation()
        onDrop()
      }}
      onDragEnd={onDragEnd}
    >
      <span className="poll-management__drag-handle" aria-hidden="true">
        <i className="fa fa-grip-vertical" />
      </span>

      {/* not a native button: Firefox does not start the parent drag from
          form controls, so the whole row doubles as the expand target */}
      <div
        className="poll-management__summary"
        role="button"
        tabIndex={0}
        aria-expanded={isExpanded}
        onClick={onEdit}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault()
            onEdit()
          }
        }}
      >
        <span className="poll-management__number">
          {index + 1}
        </span>
        <span className={'poll-management__label' + (question.label ? '' : ' poll-management__label--empty')}>
          {question.label || TRANSLATED.untitled}
        </span>
        <span className="poll-management__type">
          {typeLabel(question)}
        </span>
      </div>

      <button
        type="button"
        className="poll-management__collapse"
        onClick={onEdit}
        aria-label={isExpanded ? TRANSLATED.collapse : TRANSLATED.expand}
        title={isExpanded ? TRANSLATED.collapse : TRANSLATED.expand}
      >
        <i className={'fa ' + (isExpanded ? 'fa-chevron-up' : 'fa-chevron-down')} aria-hidden="true" />
      </button>

      {confirmingDelete
        ? (
          <div className="poll-management__delete-confirm" role="group" aria-label={TRANSLATED.deletePrompt}>
            <span className="poll-management__delete-prompt">{TRANSLATED.deletePrompt}</span>
            <button
              type="button"
              className="btn poll-management__delete-yes"
              aria-label={TRANSLATED.confirmDelete}
              title={TRANSLATED.confirmDelete}
              onClick={() => {
                setConfirmingDelete(false)
                onDelete()
              }}
            >
              <i className="fas fa-trash-alt" aria-hidden="true" />
            </button>
            <button
              type="button"
              className="btn poll-management__delete-no"
              aria-label={TRANSLATED.cancelDelete}
              title={TRANSLATED.cancelDelete}
              onClick={() => setConfirmingDelete(false)}
            >
              <i className="fas fa-times" aria-hidden="true" />
            </button>
          </div>
          )
        : (
          <button
            type="button"
            className="poll-management__delete"
            aria-label={TRANSLATED.delete}
            title={TRANSLATED.delete}
            onClick={() => setConfirmingDelete(true)}
          >
            <i className="fas fa-trash-alt" aria-hidden="true" />
          </button>
          )}
    </div>
  )
}
