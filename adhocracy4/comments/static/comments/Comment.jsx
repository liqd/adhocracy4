var ReportModal = require('../../../reports/static/reports/react_reports').ReportModal
var RatingBox = require('../../../ratings/static/ratings/react_ratings').RatingBox
var Modal = require('../../../static/Modal')
var CommentEditForm = require('./CommentEditForm')
var CommentForm = require('./CommentForm')
var CommentManageDropdown = require('./CommentManageDropdown')

var React = require('react')
var PropTypes = require('prop-types')
var django = require('django')

var safeHtml = function (text) {
  return { __html: text }
}

var localeDate = function (dateStr) {
  return new Date(dateStr).toLocaleString(document.documentElement.lang)
}

var getViewRepliesText = function (number, hide) {
  var fmts
  if (hide) {
    fmts = django.ngettext('hide one reply', 'hide %s replies', number)
  } else {
    fmts = django.ngettext('view one reply', 'view %s replies', number)
  }
  return django.interpolate(fmts, [number])
}

const answerTag = django.gettext('Answer')
const answerPlaceholderText = django.gettext('Your reply here')
const reportText = django.gettext('You want to report this content? Your message will be sent to the moderation. The moderation will look at the reported content. The content will be deleted if it does not meet our discussion rules (netiquette).')

class Comment extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      edit: false,
      showChildComments: false,
      replyFormHasFocus: false
    }
  }

  toggleEdit (e) {
    if (e) {
      e.preventDefault()
    }
    var newEdit = !this.state.edit
    this.setState({ edit: newEdit })
  }

  toggleShowComments (e) {
    e.preventDefault()
    var newShowChildComment = !this.state.showChildComments
    this.setState({
      showChildComments: newShowChildComment,
      replyFormHasFocus: false
    })
  }

  replyComments (e) {
    e.preventDefault()
    this.setState({
      showChildComments: true,
      replyFormHasFocus: true
    })
  }

  allowForm () {
    return !this.props.isReadOnly && this.props.content_type !== this.context.comments_contenttype
  }

  isOwner () {
    return this.props.user_name === this.context.user_name
  }

  renderRatingBox () {
    if (!this.props.is_deleted) {
      return (
        <RatingBox
          contentType={this.context.comments_contenttype}
          objectId={this.props.id}
          authenticatedAs={this.context.isAuthenticated ? this.context.user_name : null}
          positiveRatings={this.props.positiveRatings}
          negativeRatings={this.props.negativeRatings}
          userRating={this.props.userRating}
          userRatingId={this.props.userRatingId}
          isReadOnly={this.props.isReadOnly}
        />
      )
    }
  }

  renderModeratorLabel () {
    const moderatorTag = django.gettext('Moderator')
    if (this.props.authorIsModerator && !this.props.is_deleted) {
      return (
        <span className="label label-subtle">{moderatorTag}</span>
      )
    }
  }

  renderLastDate () {
    const lastEditText = django.gettext('Latest edit on')
    let lastDate
    if (this.props.modified === null || this.props.is_deleted) {
      lastDate = localeDate(this.props.created)
    } else {
      lastDate = lastEditText + ' ' + localeDate(this.props.modified)
    }
    return (
      <span className="comment-submission-date">{lastDate}</span>
    )
  }

  renderComment () {
    let comment
    if (this.state.edit) {
      comment = (
        <CommentEditForm
          subjectType={this.props.content_type}
          subjectId={this.props.object_pk}
          comment={this.props.children}
          error={this.props.editError}
          errorMessage={this.props.errorMessage}
          handleErrorClick={() => this.props.onEditErrorClick(this.props.index, this.props.parentIndex)}
          rows="5"
          handleCancel={this.toggleEdit.bind(this)}
          onCommentSubmit={newComment => {
            this.props.onCommentModify(newComment, this.props.index, this.props.parentIndex)
              .then(() => {
                this.setState({
                  edit: false
                })
              })
          }}
        />
      )
    } else {
      comment = <div className="comment-text" dangerouslySetInnerHTML={safeHtml(this.props.children)} />
    }
    return comment
  }

  renderDeleteModal () {
    const confirmDeleteText = django.gettext('Do you really want to delete this comment?')
    const deleteTag = django.gettext('Delete')
    const abortTag = django.gettext('Abort')
    if (this.isOwner() || this.context.isModerator) {
      return (
        <Modal
          name={`comment_delete_${this.props.id}`}
          partials={{ title: confirmDeleteText }}
          handleSubmit={() => this.props.onCommentDelete(this.props.index, this.props.parentIndex)}
          action={deleteTag}
          abort={abortTag}
          btnStyle="cta"
        />
      )
    }
  }

  render () {
    const CommentList = require('./CommentList')

    return (
      <div className="comment">
        <ReportModal
          name={`report_comment_${this.props.id}`}
          title={reportText}
          btnStyle="cta"
          objectId={this.props.id}
          contentType={this.context.comments_contenttype}
        />
        {this.renderDeleteModal()}
        <h3 className={this.props.is_deleted ? 'comment-deleted-author' : 'comment-author'}>
          {this.props.user_profile_url === '' ? this.props.user_name
            : <a href={this.props.user_profile_url} data-embed-target="external">{this.props.user_name}</a>}
          {this.renderModeratorLabel()}
        </h3>
        {this.renderLastDate()}
        {this.renderComment()}
        <div className="action-bar">
          <nav className="navbar navbar-default navbar-static">
            {this.renderRatingBox()}
            {this.allowForm() &&
              <button
                disabled={this.state.showChildComments}
                className="btn comment-answer-button"
                type="button"
                onClick={this.replyComments.bind(this)}
              >
                <i className="fa fa-reply" aria-hidden="true" /> {answerTag}
              </button>}
            {this.context.isAuthenticated && !this.props.is_deleted &&
              <CommentManageDropdown
                id={this.props.id}
                handleToggleEdit={this.toggleEdit.bind(this)}
                renderModeratorOptions={(this.isOwner() || this.context.isModerator) && !this.props.isReadOnly}
              />}
          </nav>
        </div>

        {this.props.child_comments && this.props.child_comments.length > 0 &&
          <div className="action-bar">
            <div className="navbar">
              <button className="comment-reply-button" type="button" onClick={this.toggleShowComments.bind(this)}>
                <i className={this.state.showChildComments ? 'fa fa-minus' : 'fa fa-plus'} aria-hidden="true" />
                {getViewRepliesText(this.props.child_comments.length, this.state.showChildComments)}
              </button>
            </div>
          </div>}

        <div className="comment-child-list">
          {this.state.showChildComments
            ? (
              <CommentList
                comments={this.props.child_comments}
                parentIndex={this.props.index}
                onCommentDelete={this.props.onCommentDelete}
                onCommentModify={this.props.onCommentModify}
                isReadOnly={this.props.isReadOnly}
                onEditErrorClick={this.props.onEditErrorClick}
              />) : null}

          {this.state.showChildComments && !this.props.isReadOnly && this.context.isAuthenticated
            ? (
              <CommentForm
                subjectType={this.context.comments_contenttype}
                subjectId={this.props.id}
                onCommentSubmit={this.props.onCommentSubmit}
                parentIndex={this.props.index}
                placeholder={answerPlaceholderText}
                error={this.props.replyError}
                errorMessage={this.props.errorMessage}
                handleErrorClick={() => this.props.handleReplyErrorClick(this.props.index, this.props.parentIndex)}
                rows="3"
                grabFocus={this.state.replyFormHasFocus}
              />) : null}
        </div>
      </div>
    )
  }
}

Comment.contextTypes = {
  comments_contenttype: PropTypes.number,
  isAuthenticated: PropTypes.bool,
  isModerator: PropTypes.bool,
  user_name: PropTypes.string,
  contentType: PropTypes.number
}

module.exports = Comment
