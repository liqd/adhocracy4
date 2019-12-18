import React from 'react'
import PropTypes from 'prop-types'
import django from 'django'

import * as config from '../../../static/config'
import Alert from '../../../static/Alert'

export default class CommentForm extends React.Component {
  constructor (props) {
    super(props)

    this.state = { comment: '' }
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
    }, this.props.parentIndex).then(() => {
      this.setState({ comment: '' })
    })
  }

  render () {
    if (this.context.isAuthenticated && !this.props.isReadOnly) {
      return (
        <div className="px-0 col-md-12">
          <label htmlFor="id-comment-form" className="mt-3 mb-2"> {django.gettext('The maximal length of your contribution is 4000 characters')}</label>
          <form id="id-comment-form" className="general-form" onSubmit={this.handleSubmit.bind(this)}>
            {this.props.error &&
              <Alert type="danger" message={this.props.errorMessage} onClick={this.props.handleErrorClick} />}
            <div className="form-group">
              <textarea
                rows={this.props.rows}
                className="form-control"
                placeholder={django.gettext('Write contribution')}
                onChange={this.handleTextChange.bind(this)} required="required" value={this.state.comment}
              />
            </div>
            <div className="a4-comments__submit">
              <input type="submit" value={django.gettext('post')} className="btn a4-comments__submit-input" />
            </div>
          </form>
        </div>
      )
    } else if (!this.props.isReadOnly) {
      return (
        <div className="a4-comments__login">
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
