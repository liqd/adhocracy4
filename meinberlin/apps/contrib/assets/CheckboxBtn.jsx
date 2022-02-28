import React from 'react'

export default class CheckboxBtn extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      checkedState: false
    }
  }

  handleOnChange () {
    this.setState({ checkedState: !this.state.checkedState })
  }

  render () {
    const checkedText = this.props.onText
    const uncheckedText = this.props.offText
    const checkedClass = this.props.onClass
    const uncheckedClass = this.props.offClass
    const uniqueID = this.props.uniqueID

    return (
      <div>
        <label
          htmlFor={uniqueID}
          className={this.state.checkedState ? checkedClass : uncheckedClass}
        >
          <input
            id={uniqueID}
            className="checkbox-btn__input"
            type="checkbox"
            checked={this.state.checkedState}
            onChange={(e) => this.handleOnChange(e)}
          />
          <span>{this.state.checkedState ? checkedText : uncheckedText}</span>
        </label>
      </div>
    )
  }
}
