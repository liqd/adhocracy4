var React = require('react')
var django = require('django')

var CommentEditForm = React.createClass({
  getInitialState: function () {
    return {comment: this.props.comment}
  },
  handleTextChange: function (e) {
    this.setState({comment: e.target.value})
  },
  handleSubmit: function (e) {
    e.preventDefault()
    var comment = this.state.comment.trim()
    if (!comment) {
      return
    }
    this.props.onCommentSubmit({
      comment: comment
    })
  },
  render: function () {
    return (
      <form className="general-form" onSubmit={this.handleSubmit}>
        <div className="form-group">
          <textarea rows={this.props.rows} className="form-control"
            placeholder={django.gettext('Your comment here')}
            onChange={this.handleTextChange} required="required" defaultValue={this.state.comment} />
        </div>
        <input type="submit" value={django.gettext('post')} className="submit-button" />
        <input type="submit" value={django.gettext('cancel')} className="cancel-button"
          onClick={this.props.handleCancel} />
      </form>
    )
  }
})

CommentEditForm.contextTypes = {
  isAuthenticated: React.PropTypes.bool
}

module.exports = CommentEditForm
