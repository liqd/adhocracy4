var config = require('../../../static/config')

var React = require('react')
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
    }, this.props.parentIndex)
    this.setState({comment: ''})
  }
  render () {
    if (this.context.isAuthenticated && !this.props.isReadOnly) {
      return (
        <form className="general-form" onSubmit={this.handleSubmit.bind(this)}>
          <div className="form-group">
            <textarea rows={this.props.rows} className="form-control"
              placeholder={django.gettext('Your comment here')}
              onChange={this.handleTextChange.bind(this)} required="required" value={this.state.comment} />
          </div>
          <input type="submit" value={django.gettext('post')} className="submit-button" />
        </form>
      )
    } else if (!this.context.isAuthenticated) {
      return (
        <div className="comments_login">
          <a href={config.loginUrl}>{django.gettext('Please login to comment')}</a>
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
  isAuthenticated: React.PropTypes.bool
}

module.exports = CommentForm
