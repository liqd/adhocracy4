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
      <button className="comment-reply-button" type="button" onClick={props.showComments}>
        {pluralizeString(props.childCommentsLength)}
      </button>
    )
  }

  let replyButton
  if (props.allowForm) {
    replyButton = (
      <button className="comment-reply-button" type="button" onClick={props.showComments}>
        <i className="fa fa-reply" aria-hidden="true" />
        {django.gettext('Answer')}
      </button>
    )
  }
  if (replyButton || childCommentCount) {
    return (
      <div className="action-bar">
        <div className="navbar">
          {childCommentCount}
          <div className="navbar-right">
            {replyButton}
          </div>
        </div>
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
