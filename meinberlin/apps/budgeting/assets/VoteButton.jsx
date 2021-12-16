import React from 'react'
import django from 'django'
import { updateItem } from '../../livequestions/assets/helpers.js'

export default class VoteButton extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      voted: props.isChecked
    }
  }

  componentDidMount () {
    this.setState({ voted: this.props.isChecked })
  }

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
    if (this.state.voted) {
      this.deleteVote()
    } else {
      this.addVote()
    }
    this.props.onVoteChange(this.props.currentPage)
    // this.setState({ voted: !this.state.voted })
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
          className={this.state.voted ? checkedClass : uncheckedClass}
        >
          <input
            id={this.props.objectID}
            className="checkbox-btn__input"
            type="checkbox"
            checked={this.state.voted}
            onChange={(e) => this.handleOnChange(e)}
          />
          <span>{this.state.voted ? checkedText : uncheckedText}</span>
        </label>
      </div>
    )
  }
}
