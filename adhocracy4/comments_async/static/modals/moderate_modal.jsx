import React from 'react'
import django from 'django'

import Modal from './modal'

export default class ModerateModal extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      isModeratorMarked: this.props.is_moderator_marked
    }
  }

  toggleModeratorMarked () {
    this.setState(
      { isModeratorMarked: !this.state.isModeratorMarked }
    )
  }

  render () {
    var data = {
      is_moderator_marked: this.state.isModeratorMarked,
      urlReplaces: {
        contentTypeId: this.props.content_type,
        objectPk: this.props.object_pk
      }
    }

    const partials = {}
    partials.title = django.gettext('Recommend comment')
    partials.body = (
      <div className="form-inline">
        <label htmlFor="markedCheck" className="form-check-label font-weight-bold">
          {django.gettext('Is recommended')}
        </label>
        <input
          className="form-check-input ml-4 mt-3"
          type="checkbox"
          id="markedCheck"
          name="markedCheck"
          checked={this.state.isModeratorMarked}
          onChange={this.toggleModeratorMarked.bind(this)}
        />
      </div>
    )

    return (
      <Modal
        name={`comment_moderate_${this.props.id}`}
        partials={partials}
        handleSubmit={() => this.props.onCommentModerate(data, this.props.index, this.props.parentIndex)}
        action={django.gettext('Submit')}
        abort={django.gettext('Abort')}
        btnStyle="cta"
      />
    )
  }
}
