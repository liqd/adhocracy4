var CommentList = require('./CommentList')
var CommentForm = require('./CommentForm')
var api = require('../../../static/api')

var React = require('react')
var update = require('immutability-helper')
var PropTypes = require('prop-types')
var django = require('django')

class CommentBox extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      comments: this.props.comments
    }
  }

  updateStateComment (index, parentIndex, updatedComment) {
    var comments = this.state.comments
    var diff = {}
    if (typeof parentIndex !== 'undefined') {
      diff[parentIndex] = { child_comments: {} }
      diff[parentIndex].child_comments[index] = { $merge: updatedComment }
    } else {
      diff[index] = { $merge: updatedComment }
    }
    comments = update(comments, diff)
    this.setState({ comments: comments })
  }

  handleCommentSubmit (comment, parentIndex) {
    return api.comments.add(comment)
      .done(comment => {
        var comments = this.state.comments
        var diff = {}
        if (typeof parentIndex !== 'undefined') {
          diff[parentIndex] = { child_comments: { $push: [comment] } }
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
            errorMessage: undefined
          })
        }
      })
      .fail((xhr, status, err) => {
        var errorMessage = xhr.responseJSON.comment[0]
        if (typeof parentIndex !== 'undefined') {
          this.updateStateComment(
            parentIndex,
            undefined, {
              replyError: true,
              errorMessage: errorMessage
            })
        } else {
          this.setState({
            error: true,
            errorMessage: errorMessage
          })
        }
      })
  }

  handleCommentModify (modifiedComment, index, parentIndex) {
    var comments = this.state.comments
    var comment = comments[index]
    if (typeof parentIndex !== 'undefined') {
      comment = comments[parentIndex].child_comments[index]
    }

    return api.comments.change(modifiedComment, comment.id)
      .done(changed => {
        this.updateStateComment(index, parentIndex, changed)
        this.updateStateComment(
          index,
          parentIndex, {
            editError: false,
            errorMessage: undefined
          }
        )
      })
      .fail((xhr, status, err) => {
        var errorMessage = xhr.responseJSON.comment[0]
        this.updateStateComment(
          index,
          parentIndex,
          {
            editError: true,
            errorMessage: errorMessage
          })
      })
  }

  handleCommentDelete (index, parentIndex) {
    var comments = this.state.comments
    var comment = comments[index]
    if (typeof parentIndex !== 'undefined') {
      comment = comments[parentIndex].child_comments[index]
    }

    var data = {
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
      errorMessage: undefined
    })
  }

  hideReplyError (index, parentIndex) {
    this.updateStateComment(
      index,
      parentIndex,
      {
        replyError: false,
        errorMessage: undefined
      }
    )
  }

  hideEditError (index, parentIndex) {
    this.updateStateComment(
      index,
      parentIndex,
      {
        editError: false,
        errorMessage: undefined
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
            rows="5"
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

CommentBox.childContextTypes = {
  isAuthenticated: PropTypes.bool,
  isModerator: PropTypes.bool,
  comments_contenttype: PropTypes.number,
  user_name: PropTypes.string
}

module.exports = CommentBox
