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

  handleOnChange () {
    if (this.props.isChecked) {
      this.deleteVote()
    } else {
      this.addVote()
    }
    this.props.onVoteChange(this.props.currentPage)
  }

  render () {
    const checkedText = django.gettext('Voted')
    const uncheckedText = django.gettext('Give my vote')
    const checkedClass = 'btn btn--full'
    const uncheckedClass = 'btn btn--full btn--light'

    return (
      <div>
        <label
          htmlFor={this.props.objectID}
          className={this.props.isChecked ? checkedClass : uncheckedClass}
        >
          <input
            id={this.props.objectID}
            className="checkbox-btn__input"
            type="checkbox"
            checked={this.props.isChecked}
            onChange={e => this.handleOnChange(e)}
          />
          <span>{this.props.isChecked ? checkedText : uncheckedText}</span>
        </label>
      </div>
    )
  }
}
