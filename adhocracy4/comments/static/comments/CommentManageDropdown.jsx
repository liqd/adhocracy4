var React = require('react')
var django = require('django')

const CommentManageDropdown = (props) => {
  return (
    <ul className="nav navbar-nav">
      <li className="dropdown">
        <a href="#" className="dropdown-toggle icon fa-ellipsis-h" role="button"
          aria-haspopup="true" aria-hidden="true" aria-expanded="false" data-toggle="dropdown" />
        <ul className="dropdown-menu">
          {props.renderModeratorOptions && [
            <li key="1">
              <a href="#" onClick={props.toggleEdit} aria-hidden="true">{django.gettext('Edit')}</a>
            </li>,
            <li className="divider" key="2" />,
            <li key="3"><a href={`#comment_delete_${props.id}`} data-toggle="modal"
              aria-hidden="true">{django.gettext('Delete')}</a></li>,
            <li className="divider" key="4" />
          ]}
          <li><a href={`#report_comment_${props.id}`} data-toggle="modal"
            aria-hidden="true">{django.gettext('Report')}</a>
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
