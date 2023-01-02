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
      <div className="dropdown-menu dropdown-menu-end">
        {props.has_changing_permission && [
          <button key="1" className="dropdown-item" type="button" onClick={props.handleToggleEdit}>{translated.edit}</button>,
          <div className="divider" key="2" />
        ]}
        {props.has_deleting_permission && [
          <a key="3" className="dropdown-item" href={'#comment_delete_' + props.id} data-bs-toggle="modal">{translated.delete}</a>,
          <div className="divider" key="4" />
        ]}
      </div>
    </div>
  )
}

export default CommentManageDropdown
