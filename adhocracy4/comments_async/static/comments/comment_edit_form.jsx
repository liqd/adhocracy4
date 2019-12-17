import React from 'react'
import PropTypes from 'prop-types'
import django from 'django'

import { alert as Alert } from 'adhocracy4'

export default class CommentEditForm extends React.Component {
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
    return (
      <form className="general-form" onSubmit={this.handleSubmit.bind(this)}>
        {this.props.error &&
          <Alert type="danger" message={this.props.errorMessage} onClick={this.props.handleErrorClick} />}
        <div className="form-group">
          <textarea
            rows={this.props.rows} className="form-control"
            placeholder={django.gettext('Write contribution')}
            onChange={this.handleTextChange.bind(this)} required="required" defaultValue={this.state.comment}
          />
        </div>
        <input type="submit" value={django.gettext('save changes')} className="submit-button" />
        &nbsp;
        <input
          type="submit" value={django.gettext('cancel')} className="cancel-button"
          onClick={this.props.handleCancel}
        />
      </form>
    )
  }
}

CommentEditForm.contextTypes = {
  isAuthenticated: PropTypes.bool
}
