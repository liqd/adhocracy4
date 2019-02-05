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
    this.setState({edit: newEdit})
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
          handleErrorClick={() => this.props.handleEditErrorClick(this.props.index, this.props.parentIndex)}
          rows="5"
          handleCancel={this.toggleEdit.bind(this)}
          onCommentSubmit={newComment => {
            this.props.handleCommentModify(newComment, this.props.index, this.props.parentIndex)
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
    if (this.isOwner() || this.context.isModerator) {
      return (
        <Modal
          name={`comment_delete_${this.props.id}`}
          partials={{title: django.gettext('Do you really want to delete this comment?')}}
          submitHandler={() => this.props.handleCommentDelete(this.props.index, this.props.parentIndex)}
          action={django.gettext('Delete')}
          abort={django.gettext('Abort')}
          btnStyle="cta"
        />
      )
    }
  }

  render () {
    let CommentList = require('./CommentList')
    let lastDate
    if (this.props.modified === null || this.props.is_deleted) {
      lastDate = localeDate(this.props.created)
    } else {
      lastDate = django.gettext('Latest edit on') + ' ' + localeDate(this.props.modified)
    }

    let moderatorLabel
    if (this.props.authorIsModerator && !this.props.is_deleted) {
      moderatorLabel = <span className="label label-subtle">{django.gettext('Moderator')}</span>
    }

    return (
      <div className="comment">
        <ReportModal
          name={`report_comment_${this.props.id}`}
          title={django.gettext('You want to report this content? Your message will be sent to the moderation. The moderation will look at the reported content. The content will be deleted if it does not meet our discussion rules (netiquette).')}
          btnStyle="cta"
          objectId={this.props.id}
          contentType={this.context.comments_contenttype}
        />
        {this.renderDeleteModal()}
        <h3 className={this.props.is_deleted ? 'comment-deleted-author' : 'comment-author'}>
          {this.props.is_deleted ? this.props.user_name
            : <a href={`/profile/${this.props.user_name}`} data-embed-target="external">{this.props.user_name}</a>
          }
          {moderatorLabel}
        </h3>
        <span className="comment-submission-date">{lastDate}</span>
        {this.renderComment()}
        <div className="action-bar">
          <nav className="navbar navbar-default navbar-static">
            {this.renderRatingBox()}
            {this.allowForm() &&
            <button
              disabled={this.state.showChildComments}
              className="btn comment-answer-button"
              type="button"
              onClick={this.replyComments.bind(this)}>
              <i className="fa fa-reply" aria-hidden="true" /> {django.gettext('Answer')}
            </button>
            }
            {this.context.isAuthenticated && !this.props.is_deleted &&
              <CommentManageDropdown
                id={this.props.id}
                toggleEdit={this.toggleEdit.bind(this)}
                renderModeratorOptions={(this.isOwner() || this.context.isModerator) && !this.props.isReadOnly}
              />
            }
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
          </div>
        }

        {this.state.showChildComments
          ? <div className="comment-child-list">
            <CommentList
              comments={this.props.child_comments}
              parentIndex={this.props.index}
              handleCommentDelete={this.props.handleCommentDelete}
              handleCommentModify={this.props.handleCommentModify}
              isReadOnly={this.props.isReadOnly}
              handleEditErrorClick={this.props.handleEditErrorClick}
            />
            <CommentForm
              subjectType={this.context.comments_contenttype}
              subjectId={this.props.id}
              onCommentSubmit={this.props.handleCommentSubmit}
              parentIndex={this.props.index}
              placeholder={django.gettext('Your reply here')}
              error={this.props.replyError}
              errorMessage={this.props.errorMessage}
              handleErrorClick={() => this.props.handleReplyErrorClick(this.props.index, this.props.parentIndex)}
              rows="3"
              grabFocus={this.state.replyFormHasFocus}
            />
          </div> : null
        }
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
