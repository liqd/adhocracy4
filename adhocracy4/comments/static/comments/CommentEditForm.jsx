var Alert = require('../../../static/Alert')

var React = require('react')
var PropTypes = require('prop-types')
var django = require('django')

class CommentEditForm extends React.Component {
  constructor (props) {
    super(props)

    this.state = { comment: this.props.comment }
  }

  handleTextChange (e) {
    this.setState({ comment: e.target.value })
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
    const yourCommentText = django.gettext('Your comment here')
    const saveChangesTag = django.gettext('save changes')
    const cancelTag = django.gettext('cancel')
    return (
      <form className="general-form" onSubmit={this.handleSubmit.bind(this)}>
        {this.props.error &&
          <Alert type="danger" message={this.props.errorMessage} onClick={this.props.handleErrorClick} />}
        <div className="form-group">
          <textarea
            rows={this.props.rows} className="form-control"
            placeholder={yourCommentText}
            onChange={this.handleTextChange.bind(this)} required="required" defaultValue={this.state.comment}
          />
        </div>
        <input type="submit" value={saveChangesTag} className="submit-button" />
        &nbsp;
        <input
          type="submit" value={cancelTag} className="cancel-button"
          onClick={this.props.handleCancel}
        />
      </form>
    )
  }
}

CommentEditForm.contextTypes = {
  isAuthenticated: PropTypes.bool
}

module.exports = CommentEditForm
