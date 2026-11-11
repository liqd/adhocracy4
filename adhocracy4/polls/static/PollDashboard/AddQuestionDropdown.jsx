import React from 'react'
import django from 'django'

const TRANSLATED = {
  newQuestion: django.gettext('New question'),
  multipleChoice: django.gettext('Multiple choice'),
  open: django.gettext('Open question')
}

export const AddQuestionDropdown = ({ onAddMultipleChoice, onAddOpen }) => (
  <div className="dropdown poll-management__add-dropdown">
    <button
      type="button"
      className="dropdown-toggle btn btn--light"
      aria-haspopup="true"
      aria-expanded="false"
      data-bs-toggle="dropdown"
    >
      <i className="fa fa-plus" aria-hidden="true" />
      {' '}
      {TRANSLATED.newQuestion}
    </button>
    <div className="dropdown-menu">
      <button type="button" className="dropdown-item" onClick={onAddMultipleChoice}>
        {TRANSLATED.multipleChoice}
      </button>
      <button type="button" className="dropdown-item" onClick={onAddOpen}>
        {TRANSLATED.open}
      </button>
    </div>
  </div>
)
