const config = require('../../../static/config')
const Alert = require('../../../static/Alert')

const React = require('react')
const django = require('django')

class CommentForm extends React.Component {
  constructor (props) {
    super(props)

    this.state = { comment: '' }
  }

  handleTextChange (e) {
    this.setState({ comment: e.target.value })
  }

  handleSubmit (e) {
    e.preventDefault()
    const comment = this.state.comment.trim()
    if (!comment) {
      return
    }
    this.props.onCommentSubmit({
      comment,
      urlReplaces: {
        objectPk: this.props.subjectId,
        contentTypeId: this.props.subjectType
      }
    }, this.props.parentIndex)
      .then(() => {
        this.setState({ comment: '' })
        return null
      })
      .catch(error => console.warn(error))
  }

  render () {
    const postTag = django.gettext('post')
    const loginCommentText = django.gettext('Please login to comment')
    const noCommentText = django.gettext('The currently active phase doesn\'t allow to comment.')
    const noCommentTextSemiPub = django.gettext('Only invited users can actively participate.')

    if (this.context.isAuthenticated && !this.props.isReadOnly) {
      return (
        <form className="general-form" onSubmit={this.handleSubmit.bind(this)}>
          {this.props.error &&
            <Alert type="danger" message={this.props.errorMessage} onClick={this.props.handleErrorClick} />}
          <div className="form-group">
            <textarea
              autoFocus={this.props.grabFocus} // eslint-disable-line jsx-a11y/no-autofocus
              rows={this.props.rows}
              className="form-control"
              placeholder={this.props.placeholder}
              onChange={this.handleTextChange.bind(this)} required="required" value={this.state.comment}
            />
          </div>
          <input type="submit" value={postTag} className="submit-button" />
        </form>
      )
    } else if (!this.props.isReadOnly) {
      return (
        <div className="comments_login">
          <a href={config.getLoginUrl()}>{loginCommentText}</a>
        </div>
      )
    } else if (!this.props.isContextMember) {
      return (
        <div>
          {noCommentTextSemiPub}
        </div>
      )
    } else {
      return (
        <div>
          {noCommentText}
        </div>
      )
    }
  }
}

module.exports = CommentForm
