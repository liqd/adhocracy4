var React = require('react')
var PropTypes = require('prop-types')
var django = require('django')

class CommentEditForm extends React.Component {
  constructor (props) {
    super(props)

    this.state = {comment: this.props.comment}
  }
  handleTextChange (e) {
    this.setState({comment: e.target.value})
  }
  handleSubmit (e) {
    e.preventDefault()
    var comment = this.state.comment.trim()
    if (!comment) {
      return
    }
    this.props.onCommentSubmit({
      comment: comment,
      urlReplaces: {
        objectPk: this.props.subjectId,
        contentTypeId: this.props.subjectType
      }
    })
  }
  render () {
    return (
      <form className="general-form" onSubmit={this.handleSubmit.bind(this)}>
        <div className="form-group">
          <textarea rows={this.props.rows} className="form-control"
            placeholder={django.gettext('Your comment here')}
            onChange={this.handleTextChange.bind(this)} required="required" defaultValue={this.state.comment.bind(this)} />
        </div>
        <input type="submit" value={django.gettext('post')} className="submit-button" />
        <input type="submit" value={django.gettext('cancel')} className="cancel-button"
          onClick={this.props.handleCancel} />
      </form>
    )
  }
}

CommentEditForm.contextTypes = {
  isAuthenticated: PropTypes.bool
}

module.exports = CommentEditForm
