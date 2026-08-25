/* eslint-disable no-restricted-syntax */
import React from 'react'
import django from 'django'

import Modal from '../../../static/Modal'
import { ReportModal } from '../../../reports/static/reports/react_reports'
import RatingBox from '../../../ratings/static/ratings/RatingBox'
import CommentEditForm from './CommentEditForm'
import CommentForm from './CommentForm'
import CommentList from './CommentList'
import CommentManageDropdown from './CommentManageDropdown'
import type { Comment as CommentType, CommentPayload } from '../../../static/api/types'

const localeDate = function (dateStr: string) {
  return new Date(dateStr).toLocaleString(document.documentElement.lang)
}

const getViewRepliesText = function (number: number, hide: boolean) {
  let fmts
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

interface CommentProps {
  user_name: string
  user_profile_url: string
  child_comments: CommentType[]
  created: string
  modified: string | null
  authorIsModerator: boolean
  id: number
  content_type: number
  object_pk: number
  is_deleted: boolean
  is_removed: boolean
  is_censored: boolean
  index: number
  parentIndex?: number
  onCommentDelete: (index: number, parentIndex?: number) => void
  onCommentSubmit: (comment: CommentPayload, parentIndex?: number) => any
  onCommentModify: (comment: CommentPayload, index: number, parentIndex?: number) => any
  positiveRatings: number
  negativeRatings: number
  userRating: number | null
  userRatingId: number | null
  isReadOnly: boolean
  replyError?: boolean
  errorMessage?: string
  onReplyErrorClick: (index: number, parentIndex?: number) => void
  editError?: boolean
  onEditErrorClick: (index: number, parentIndex?: number) => void
  children: string
}

interface CommentContext {
  isAuthenticated: boolean
  isModerator: boolean
  comments_contenttype: number
  user_name: string
}

interface CommentState {
  edit: boolean
  showChildComments: boolean
  replyFormHasFocus: boolean
}

class Comment extends React.Component<CommentProps, CommentState> {
  static contextType = React.createContext<CommentContext>({} as CommentContext)

  declare context: CommentContext

  constructor (props: CommentProps) {
    super(props)

    this.state = {
      edit: false,
      showChildComments: false,
      replyFormHasFocus: false
    }
  }

  toggleEdit (e?: React.MouseEvent) {
    if (e) {
      e.preventDefault()
    }
    const newEdit = !this.state.edit
    this.setState({ edit: newEdit })
  }

  toggleShowComments (e: React.MouseEvent) {
    e.preventDefault()
    const newShowChildComment = !this.state.showChildComments
    this.setState({
      showChildComments: newShowChildComment,
      replyFormHasFocus: false
    })
  }

  replyComments (e: React.MouseEvent) {
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
          isComment
        />
      )
    }
    return null
  }

  renderModeratorLabel () {
    const moderatorTag = django.gettext('Moderator')
    if (this.props.authorIsModerator && !this.props.is_deleted) {
      return (
        <span className="label label-subtle">{moderatorTag}</span>
      )
    }
    return null
  }

  renderLastDate () {
    const lastEditText = django.gettext('Latest edit on')
    let lastDate
    if (this.props.modified === null) {
      lastDate = localeDate(this.props.created)
    } else if (this.props.is_removed) {
      lastDate = django.gettext('Deleted by creator on') + ' ' + localeDate(this.props.modified)
    } else if (this.props.is_censored) {
      lastDate = django.gettext('Deleted by moderator on') + ' ' + localeDate(this.props.modified)
    } else {
      lastDate = lastEditText + ' ' + localeDate(this.props.modified)
    }
    return (
      <span className="comment-submission-date">{lastDate}</span>
    )
  }

  renderComment () {
    let comment: React.ReactNode
    if (this.state.edit) {
      comment = (
        <CommentEditForm
          subjectType={this.props.content_type}
          subjectId={this.props.object_pk}
          comment={this.props.children}
          error={this.props.editError}
          errorMessage={this.props.errorMessage}
          handleErrorClick={() => this.props.onEditErrorClick(this.props.index, this.props.parentIndex)}
          rows={5}
          handleCancel={this.toggleEdit.bind(this)}
          onCommentSubmit={newComment => {
            this.props.onCommentModify(newComment, this.props.index, this.props.parentIndex)
              .then(() => {
                this.setState({
                  edit: false
                })
                return null
              })
              .catch((error: Error) => console.warn(error))
          }}
        />
      )
    } else {
      comment = <div className="comment-text" dangerouslySetInnerHTML={{ __html: this.props.children }} />
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
          partials={{
            title: deleteTag,
            description: confirmDeleteText
          }}
          handleSubmit={() => this.props.onCommentDelete(this.props.index, this.props.parentIndex)}
          action={deleteTag}
          toggle={<span>{abortTag}</span>}
        />
      )
    }
    return null
  }

  render () {
    return (
      <div className="comment">
        <ReportModal
          name={'report_comment_' + this.props.id}
          description={reportText}
          objectId={this.props.id}
          contentType={this.context.comments_contenttype}
        />
        {this.renderDeleteModal()}
        <h3 className={this.props.is_deleted ? 'comment-deleted-author' : 'comment-author'}>
          {this.props.user_profile_url === ''
            ? this.props.user_name
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
                aria-disabled={this.state.showChildComments}
                aria-expanded={this.state.showChildComments && this.state.replyFormHasFocus}
                aria-controls={`reply-form-${this.props.id}`}
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
              <button
                className="comment-reply-button"
                type="button"
                onClick={this.toggleShowComments.bind(this)}
                aria-expanded={this.state.showChildComments}
                aria-controls={`child-comments-${this.props.id}`}
              >
                <i className={this.state.showChildComments ? 'fa fa-minus' : 'fa fa-plus'} aria-hidden="true" />
                {getViewRepliesText(this.props.child_comments.length, this.state.showChildComments)}
              </button>
            </div>
          </div>}

        <div className="comment-child-list" id={`child-comments-${this.props.id}`}>
          {this.state.showChildComments
            ? (
              <CommentList
                comments={this.props.child_comments}
                parentIndex={this.props.index}
                onCommentDelete={this.props.onCommentDelete}
                onCommentSubmit={this.props.onCommentSubmit}
                onCommentModify={this.props.onCommentModify}
                isReadOnly={this.props.isReadOnly}
                onReplyErrorClick={this.props.onReplyErrorClick}
                onEditErrorClick={this.props.onEditErrorClick}
              />)
            : null}

          {this.state.showChildComments && !this.props.isReadOnly && this.context.isAuthenticated
            ? (
              <CommentForm
                id={`reply-form-${this.props.id}`}
                subjectType={this.context.comments_contenttype}
                subjectId={this.props.id}
                onCommentSubmit={this.props.onCommentSubmit}
                parentIndex={this.props.index}
                placeholder={answerPlaceholderText}
                error={this.props.replyError}
                errorMessage={this.props.errorMessage}
                handleErrorClick={() => this.props.onReplyErrorClick(this.props.index, this.props.parentIndex)}
                rows={3}
                isReadOnly={this.props.isReadOnly}
                grabFocus={this.state.replyFormHasFocus}
              />)
            : null}
        </div>
      </div>
    )
  }
}

export default Comment
