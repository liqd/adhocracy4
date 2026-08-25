// DEPRECATED: this component tree is superseded by
// comments_async/static/comments_async. Kept for backwards compatibility
// with consumers still importing the legacy comments module.
import React from 'react'
import django from 'django'
import Alert from '../../../static/Alert'

interface CommentEditFormProps {
  comment: string
  error?: any
  errorMessage?: string
  handleErrorClick: () => void
  onCommentSubmit: (comment: any) => void
  subjectId: number
  subjectType: number
  rows: number
  handleCancel: () => void
}

interface CommentEditFormState {
  comment: string
}

class CommentEditForm extends React.Component<CommentEditFormProps, CommentEditFormState> {
  constructor (props: CommentEditFormProps) {
    super(props)

    this.state = { comment: this.props.comment }
  }

  handleTextChange (e: React.ChangeEvent<HTMLTextAreaElement>) {
    this.setState({ comment: e.target.value })
  }

  handleSubmit (e: React.FormEvent) {
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
            onChange={this.handleTextChange.bind(this)} required defaultValue={this.state.comment}
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

export default CommentEditForm
