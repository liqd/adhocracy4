
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
    var categoryChoices = this.props.commentCategoryChoices
    let categoryCheck = ''
    let inputId = ''

    var categoryChoiceHtml = Object.keys(categoryChoices).map(function (objectKey, index) {
      categoryCheck = categoryChoices[objectKey]
      inputId = 'id_' + {objectKey}
      return (
        <div className="form-group_category" key={objectKey}>
          <label className="form-group_category_row" htmlFor={inputId} for={inputId}>
            <input className="form-group_input_category" type="checkbox" id={inputId} value={categoryCheck}/>
            {categoryCheck}
          </label>
        </div>
      )
    })

    if (this.context.isAuthenticated && !this.props.isReadOnly) {
      return (
        <form className="general-form" onSubmit={this.handleSubmit.bind(this)}>
          {this.props.error &&
            <Alert type="danger" message={this.props.errorMessage} onClick={this.props.handleErrorClick} />
          }
          <div className="form-group">
            <fieldset>
              <legend className="sr-only">{django.gettext('Choose categories for your comment')}</legend>
              {categoryChoiceHtml}
            </fieldset>
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
  isAuthenticated: PropTypes.bool,
  commentCategoryChoices: PropTypes.object
}

module.exports = CommentForm
