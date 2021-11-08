import React from 'react'
import PropTypes from 'prop-types'
import django from 'django'

const CommentManageDropdown = (props) => {
  return (
    <div className="nav navbar-nav">
      <div className="dropdown a4-comments__dropdown dropend">
        <button
          type="button"
          className="dropdown-toggle btn btn--end"
          aria-haspopup="true"
          aria-expanded="false"
          data-bs-toggle="dropdown"
        >
          <i className="fas fa-ellipsis-v" aria-hidden="true" />
        </button>
        <ul className="dropdown-menu">
          {props.renderOwnerOptions &&
            <a className="dropdown-item" type="button" onClick={props.handleToggleEdit}>{django.gettext('Edit')}</a>}
          {(props.renderOwnerOptions || props.renderModeratorOptions) && [
            <a key="1" className="dropdown-item" href={`#comment_delete_${props.id}`} data-bs-toggle="modal">{django.gettext('Delete')}</a>
          ]}
          {!props.renderOwnerOptions && props.renderModeratorOptions &&
            <a className="dropdown-item" href={`#comment_block_${props.id}`} data-bs-toggle="modal">{django.gettext('Block')}</a>}
        </ul>
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
