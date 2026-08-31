// DEPRECATED: this component tree is superseded by
// comments_async/static/comments_async. Kept for backwards compatibility
// with consumers still importing the legacy comments module.
import React from 'react'
import update, { type Spec } from 'immutability-helper'
import django from 'django'
import api from '../../../static/api'
import type { Comment, CommentPayload } from '../../../static/api/types'
import CommentList from './CommentList'
import CommentForm from './CommentForm'

interface CommentBoxProps {
  comments: Comment[]
  isAuthenticated: boolean
  isModerator: boolean
  comments_contenttype: number
  user_name: string
  subjectType: number
  subjectId: number
  isReadOnly: boolean
  isContextMember: boolean
}

interface CommentBoxState {
  comments: Comment[]
  error: boolean
  errorMessage: string
}

class CommentBox extends React.Component<CommentBoxProps, CommentBoxState> {
  constructor (props: CommentBoxProps) {
    super(props)

    this.state = {
      comments: this.props.comments,
      error: false,
      errorMessage: ''
    }
  }

  updateStateComment (index: number, parentIndex: number | undefined, updatedComment: Partial<Comment>) {
    let comments = this.state.comments
    let diff: Spec<Comment[]>
    if (typeof parentIndex !== 'undefined') {
      diff = {
        [parentIndex]: {
          child_comments: {
            [index]: { $merge: updatedComment }
          }
        }
      }
    } else {
      diff = {
        [index]: { $merge: updatedComment }
      }
    }
    comments = update(comments, diff)
    this.setState({ comments })
  }

  handleCommentSubmit (comment: CommentPayload, parentIndex?: number) {
    return api.comments.add(comment)
      .done((comment: Comment) => {
        const comments = this.state.comments
        let diff: Spec<Comment[]>
        if (typeof parentIndex !== 'undefined') {
          diff = { [parentIndex]: { child_comments: { $push: [comment] } } }
        } else {
          diff = { $unshift: [comment] }
        }
        this.setState({
          comments: update(comments, diff)
        })

        if (typeof parentIndex !== 'undefined') {
          this.updateStateComment(
            parentIndex,
            undefined,
            {
              replyError: false,
              errorMessage: undefined
            })
        } else {
          this.setState({
            error: false,
            errorMessage: ''
          })
        }
      })
      .fail((xhr: JQuery.jqXHR<Comment>, _status: any, _err: any) => {
        const errorMessage = String(xhr.responseJSON?.comment?.[0] ?? '')
        if (typeof parentIndex !== 'undefined') {
          this.updateStateComment(
            parentIndex,
            undefined, {
              replyError: true,
              errorMessage
            })
        } else {
          this.setState({
            error: true,
            errorMessage
          })
        }
      })
  }

  handleCommentModify (modifiedComment: CommentPayload, index: number, parentIndex?: number) {
    const comments = this.state.comments
    let comment = comments[index]
    if (typeof parentIndex !== 'undefined') {
      comment = comments[parentIndex].child_comments[index]
    }

    return api.comments.change(modifiedComment, comment.id)
      .done((changed: Comment) => {
        this.updateStateComment(index, parentIndex, changed)
        this.updateStateComment(
          index,
          parentIndex, {
            editError: false,
            errorMessage: ''
          }
        )
      })
      .fail((xhr: JQuery.jqXHR<Comment>, _status: any, _err: any) => {
        const errorMessage = String(xhr.responseJSON?.comment?.[0] ?? '')
        this.updateStateComment(
          index,
          parentIndex,
          {
            editError: true,
            errorMessage
          })
      })
  }

  handleCommentDelete (index: number, parentIndex?: number) {
    const comments = this.state.comments
    let comment = comments[index]
    if (typeof parentIndex !== 'undefined') {
      comment = comments[parentIndex].child_comments[index]
    }

    const data = {
      urlReplaces: {
        contentTypeId: comment.content_type,
        objectPk: comment.object_pk
      }
    }
    return api.comments.delete(data, comment.id)
      .done(this.updateStateComment.bind(this, index, parentIndex))
  }

  hideNewError () {
    this.setState({
      error: false,
      errorMessage: ''
    })
  }

  hideReplyError (index: number, parentIndex?: number) {
    this.updateStateComment(
      index,
      parentIndex,
      {
        replyError: false,
        errorMessage: ''
      }
    )
  }

  hideEditError (index: number, parentIndex?: number) {
    this.updateStateComment(
      index,
      parentIndex,
      {
        editError: false,
        errorMessage: ''
      }
    )
  }

  getChildContext () {
    return {
      isAuthenticated: this.props.isAuthenticated,
      isModerator: this.props.isModerator,
      comments_contenttype: this.props.comments_contenttype,
      user_name: this.props.user_name
    }
  }

  render () {
    const yourCommentText = django.gettext('Your comment here')
    return (
      <div>
        <div className="black-divider">{this.state.comments.length + ' ' + django.ngettext('comment', 'comments', this.state.comments.length)}</div>
        <div className="comment-box">
          <CommentForm
            subjectType={this.props.subjectType}
            subjectId={this.props.subjectId}
            onCommentSubmit={this.handleCommentSubmit.bind(this)}
            placeholder={yourCommentText}
            rows={5}
            isReadOnly={this.props.isReadOnly}
            error={this.state.error}
            errorMessage={this.state.errorMessage}
            handleErrorClick={this.hideNewError.bind(this)}
            isContextMember={this.props.isContextMember}
          />
          <div className="comment-list">
            <CommentList
              comments={this.state.comments}
              onCommentDelete={this.handleCommentDelete.bind(this)}
              onCommentSubmit={this.handleCommentSubmit.bind(this)}
              onCommentModify={this.handleCommentModify.bind(this)}
              isReadOnly={this.props.isReadOnly}
              onReplyErrorClick={this.hideReplyError.bind(this)}
              onEditErrorClick={this.hideEditError.bind(this)}
            />
          </div>
        </div>
      </div>
    )
  }
}

export default CommentBox
