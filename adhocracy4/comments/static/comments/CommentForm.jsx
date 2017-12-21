var config = require('../../../static/config')
var Alert = require('../../../static/Alert')

var React = require('react')
var PropTypes = require('prop-types')
var django = require('django')

class CommentForm extends React.Component {
  constructor (props) {
    super(props)

    this.state = {comment: ''}
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
    }, this.props.parentIndex).then(() => {
      this.setState({comment: ''})
    })
  }

  render () {
    if (this.context.isAuthenticated && !this.props.isReadOnly) {
      return (
        <form className="general-form" onSubmit={this.handleSubmit.bind(this)}>
          {this.props.error &&
            <Alert type="danger" message={django.gettext('Error while submitting your comment!')} onClick={this.props.handleErrorClick} />
          }
          <div className="form-group">
            <textarea
              autoFocus={this.props.grabFocus}
              rows={this.props.rows}
              className="form-control"
              placeholder={django.gettext('Your comment here')}
              onChange={this.handleTextChange.bind(this)} required="required" value={this.state.comment} />
          </div>
          <input type="submit" value={django.gettext('post')} className="submit-button" />
        </form>
      )
    } else if (!this.props.isReadOnly) {
      return (
        <div className="comments_login">
          <a href={config.getLoginUrl()}>{django.gettext('Please login to comment')}</a>
        </div>
      )
    } else {
      return (
        <div>
          {django.gettext('The currently active phase doesn\'t allow to comment.')}
        </div>
      )
    }
  }
}

CommentForm.contextTypes = {
  isAuthenticated: PropTypes.bool
}

module.exports = CommentForm
