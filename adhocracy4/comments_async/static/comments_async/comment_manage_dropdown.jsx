import React from 'react'
import django from 'django'

const translated = {
  edit: django.gettext('Edit'),
  delete: django.gettext('Delete')
}

const CommentManageDropdown = (props) => {
  return (
    <div className="dropdown a4-comments__dropdown">
      <button
        type="button"
        className="dropdown-toggle btn btn--link"
        aria-haspopup="true"
        aria-expanded="false"
        data-bs-toggle="dropdown"
      >
        <i className="fas fa-ellipsis-h" aria-hidden="true" />
      </button>
      <ul className="dropdown-menu dropdown-menu-end">
        {props.has_changing_permission && (
          <li className="dropdown-item">
            <button type="button" onClick={props.handleToggleEdit}>
              {translated.edit}
            </button>
          </li>
        )}
        {props.has_deleting_permission && (
          <li className="dropdown-item">
            {props.modals.deleteModal}
          </li>
        )}
      </ul>
    </div>
  )
}

export default CommentManageDropdown
