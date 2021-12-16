import React from 'react'
import PropTypes from 'prop-types'
import django from 'django'

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
        {(props.renderOwnerOptions || props.renderModeratorOptions) && [
          <button key="1" className="dropdown-item" type="button" onClick={props.handleToggleEdit}>{django.gettext('Edit')}</button>,
          <div className="divider" key="2" />,
          <a key="3" className="dropdown-item" href={`#comment_delete_${props.id}`} data-bs-toggle="modal">{django.gettext('Delete')}</a>,
          <div className="divider" key="4" />
        ]}
      </div>
    </div>
  )
}

CommentManageDropdown.propTypes = {
  handleToggleEdit: PropTypes.func,
  id: PropTypes.number,
  renderModeratorOptions: PropTypes.bool
}

export default CommentManageDropdown
