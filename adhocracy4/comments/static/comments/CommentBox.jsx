var CommentList = require('./CommentList')
var CommentForm = require('./CommentForm')
var api = require('../../../static/api')

var React = require('react')
var update = require('immutability-helper')
var django = require('django')

let CommentBox = React.createClass({
  updateStateComment: function (index, parentIndex, updatedComment) {
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
  },
  handleCommentSubmit: function (comment, parentIndex) {
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
  },
  handleCommentModify: function (modifiedComment, index, parentIndex) {
    var comments = this.state.comments
    var comment = comments[index]
    if (typeof parentIndex !== 'undefined') {
      comment = comments[parentIndex].child_comments[index]
    }

    api.comments.change(modifiedComment, comment.id)
      .done(this.updateStateComment.bind(this, index, parentIndex))
  },
  handleCommentDelete: function (index, parentIndex) {
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
  },
  getInitialState: function () {
    return {
      comments: this.props.comments
    }
  },
  getChildContext: function () {
    return {
      isAuthenticated: this.props.isAuthenticated,
      isModerator: this.props.isModerator,
      comments_contenttype: this.props.comments_contenttype,
      user_name: this.props.user_name
    }
  },
  render: function () {
    return (
      <div>
        <div className="black-divider">{this.state.comments.length + ' ' + django.ngettext('comment', 'comments', this.state.comments.length)}</div>
        <div className="comment-box">
          <CommentForm subjectType={this.props.subjectType} subjectId={this.props.subjectId}
            onCommentSubmit={this.handleCommentSubmit} placeholder={django.gettext('Your comment here')}
            rows="5" isReadOnly={this.props.isReadOnly} />
          <div className="comment-list">
            <CommentList comments={this.state.comments} handleCommentDelete={this.handleCommentDelete}
              handleCommentSubmit={this.handleCommentSubmit} handleCommentModify={this.handleCommentModify}
              isReadOnly={this.props.isReadOnly} />
          </div>
        </div>
      </div>
    )
  }
})

CommentBox.childContextTypes = {
  isAuthenticated: React.PropTypes.bool,
  isModerator: React.PropTypes.bool,
  comments_contenttype: React.PropTypes.number,
  user_name: React.PropTypes.string
}

module.exports = CommentBox
