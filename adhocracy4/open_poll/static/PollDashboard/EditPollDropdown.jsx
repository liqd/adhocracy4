import React from 'react'
import django from 'django'

const translated = {
  new: django.gettext(' New Question'),
  multi: django.gettext('Multiple Choice question'),
  open: django.gettext('Open question')
}

const EditPollDropdown = (props) => {
  return (
    <div className="dropdown editpoll__dropdown">
      <button
        type="button"
        className="dropdown-toggle btn btn--light"
        aria-haspopup="true"
        aria-expanded="false"
        data-bs-toggle="dropdown"
      >
        <i className="fa fa-plus" />
        {translated.new}
      </button>
      <div className="dropdown-menu">
        <button
          key="1"
          className="dropdown-item"
          type="button"
          onClick={props.handleToggleMulti}
        >
          {translated.multi}
        </button>
        <button
          key="2"
          className="dropdown-item"
          type="button"
          onClick={props.handleToggleOpen}
        >
          {translated.open}
        </button>
      </div>
    </div>
  )
}

export default EditPollDropdown
