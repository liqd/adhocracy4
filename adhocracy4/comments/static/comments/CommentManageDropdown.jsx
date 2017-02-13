var React = require('react')
var django = require('django')

const CommentManageDropdown = (props) => {
  return (
    <ul className="nav navbar-nav">
      <li className="dropdown">
        <button type="button" className="dropdown-toggle" aria-haspopup="true"
          aria-expanded="false" data-toggle="dropdown">
          <i className="fa fa-ellipsis-h" aria-hidden="true"></i>
        </button>
        <ul className="dropdown-menu">
          {props.renderModeratorOptions && [
            <li key="1">
              <button type="button" className="dropdown-item" onClick={props.toggleEdit}>{django.gettext('Edit')}</button>
            </li>,
            <li className="divider" key="2" />,
            <li key="3"><a className="dropdown-item" href={`#comment_delete_${props.id}`} data-toggle="modal"
              >{django.gettext('Delete')}</a></li>,
            <li className="divider" key="4" />
          ]}
          <li><a className="dropdown-item" href={`#report_comment_${props.id}`} data-toggle="modal"
            >{django.gettext('Report')}</a>
          </li>
        </ul>
      </li>
    </ul>
  )
}

CommentManageDropdown.propTypes = {
  toggleEdit: React.PropTypes.func,
  id: React.PropTypes.number,
  renderModeratorOptions: React.PropTypes.bool
}

module.exports = CommentManageDropdown
