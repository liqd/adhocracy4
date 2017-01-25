var React = require('react')
var django = require('django')

function pluralizeString (number) {
  var fmts = django.ngettext('view %s reply',
    'view %s replies', number)
  return django.interpolate(fmts, [number])
}

const CommentReplyBar = (props) => {
  let childCommentCount
  if (props.childCommentsLength > 0) {
    childCommentCount = (
      <ul className="nav navbar-nav">
        <li className="entry">
          <button type="button" onClick={props.showComments}>{pluralizeString(props.childCommentsLength)}</button>
        </li>
      </ul>
    )
  }

  let replyButton
  if (props.allowForm) {
    replyButton = (
      <ul className="nav navbar-nav navbar-right">
        <li className="entry">
          <button type="button" onClick={props.showComments}>
            <i className="fa fa-reply" aria-hidden="true"></i>
            {django.gettext('Answer')}
          </button>
        </li>
      </ul>
    )
  }
  if (replyButton || childCommentCount) {
    return (
      <div className="action-bar">
        <nav className="navbar navbar-default navbar-static">
          {childCommentCount}
          {replyButton}
        </nav>
      </div>
    )
  } else {
    return null
  }
}

CommentReplyBar.propTypes = {
  childCommentsLength: React.PropTypes.number,
  showComments: React.PropTypes.func,
  allowForm: React.PropTypes.bool
}

module.exports = CommentReplyBar
