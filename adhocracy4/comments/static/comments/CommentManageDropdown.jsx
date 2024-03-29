const React = require('react')
const django = require('django')

const CommentManageDropdown = (props) => {
  const editTag = django.gettext('Edit')
  const deleteTag = django.gettext('Delete')
  const reportTag = django.gettext('Report')
  return (
    <ul className="nav navbar-nav">
      <li className="dropdown">
        <button
          type="button" className="dropdown-toggle" aria-haspopup="true"
          aria-expanded="false" data-bs-toggle="dropdown"
        >
          <i className="fa fa-ellipsis-h" aria-hidden="true" />
        </button>
        <ul className="dropdown-menu">
          {props.renderModeratorOptions && [
            <li key="1">
              <button type="button" onClick={props.handleToggleEdit}>{editTag}</button>
            </li>,
            <li className="divider" key="2" />,
            <li key="3"><a href={'#comment_delete_' + props.id} data-bs-toggle="modal">{deleteTag}</a></li>,
            <li className="divider" key="4" />
          ]}
          <li><a href={'#report_comment_' + props.id} data-bs-toggle="modal">{reportTag}</a>
          </li>
        </ul>
      </li>
    </ul>
  )
}

module.exports = CommentManageDropdown
