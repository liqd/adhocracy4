import React from 'react'
import django from 'django'
import { updateItem } from '../../contrib/assets/helpers.js'

export default class VoteButton extends React.Component {
  async addVote () {
    const data = {
      object_id: this.props.objectID
    }
    await updateItem(data, this.props.tokenvoteApiUrl, 'POST')
  }

  async deleteVote () {
    const url = this.props.tokenvoteApiUrl + this.props.objectID + '/'
    await updateItem({}, url, 'DELETE')
  }

  triggerRender = () => {
    // FIXME: this distuingishes between if
    // it has a parent that handles onVoteChange
    // or if it is used as widget, and therefore page
    // has to be reloaded --> fix would be one asynchronous way
    if (this.props.asWidget) {
      window.location.reload()
    } else {
      this.props.onVoteChange(this.props.currentPage)
    }
  }

  async handleOnChange () {
    if (this.props.isChecked) {
      await this.deleteVote()
    } else {
      await this.addVote()
    }
    this.triggerRender()
  }

  render () {
    const checkedText = django.gettext('Voted')
    const uncheckedText = django.gettext('Give my vote')
    const checkedClass = 'btn btn--full btn--primary'
    const uncheckedClass = 'btn btn--full btn--light'
    const disabledClass = ' is-disabled'

    return (
      <div>
        <label
          htmlFor={this.props.objectID}
          className={this.props.isChecked ? checkedClass : uncheckedClass + (this.props.disabled ? disabledClass : '')}
        >
          <input
            id={this.props.objectID}
            className="radio__input"
            type="checkbox"
            disabled={this.props.disabled}
            checked={this.props.isChecked}
            onChange={e => this.handleOnChange(e)}
            onKeyDown={e => event.key === 'Enter' && this.handleOnChange(e)}
          />
          <span>{this.props.isChecked ? checkedText : uncheckedText}</span>
        </label>
      </div>
    )
  }
}
