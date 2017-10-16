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
    api.comments.add(comment)
      .done(function (comment) {
        var comments = this.state.comments
        var diff = {}
        if (typeof parentIndex !== 'undefined') {
          diff[parentIndex] = { child_comments: { $push: [ comment ] } }
        } else {
          diff = { $unshift: [ comment ] }
        }
        this.setState({
          comments: update(comments, diff)
        })
      }.bind(this))
  }
  handleCommentModify (modifiedComment, index, parentIndex) {
    var comments = this.state.comments
    var comment = comments[index]
    if (typeof parentIndex !== 'undefined') {
      comment = comments[parentIndex].child_comments[index]
    }

    api.comments.change(modifiedComment, comment.id)
      .done(this.updateStateComment.bind(this, index, parentIndex))
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
    api.comments.delete(data, comment.id)
      .done(this.updateStateComment.bind(this, index, parentIndex))
  }
  getChildContext () {
    return {
      isAuthenticated: this.props.isAuthenticated,
      isModerator: this.props.isModerator,
      comments_contenttype: this.props.comments_contenttype,
      user_name: this.props.user_name,
      would_comment_perm: this.props.would_comment_perm
    }
  }
  render () {
    return (
      <div>
        <div className="black-divider">{this.state.comments.length + ' ' + django.ngettext('comment', 'comments', this.state.comments.length)}</div>
        <div className="comment-box">
          <CommentForm subjectType={this.props.subjectType} subjectId={this.props.subjectId}
            onCommentSubmit={this.handleCommentSubmit.bind(this)} placeholder={django.gettext('Your comment here')}
            rows="5" isReadOnly={this.props.isReadOnly} />
          <div className="comment-list">
            <CommentList comments={this.state.comments} handleCommentDelete={this.handleCommentDelete.bind(this)}
              handleCommentSubmit={this.handleCommentSubmit.bind(this)} handleCommentModify={this.handleCommentModify.bind(this)}
              isReadOnly={this.props.isReadOnly} />
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
  user_name: PropTypes.string,
  would_comment_perm: PropTypes.bool
}

module.exports = CommentBox
