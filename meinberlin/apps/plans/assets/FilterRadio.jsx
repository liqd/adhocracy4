/* global django */
const React = require('react')
const allStr = django.gettext('all')

class FilterRadio extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      selectedChoice: this.props.chosen
    }
  }

  handleOnChange (event) {
    const choiceId = parseInt(event.target.value)
    this.props.onSelect(choiceId)
    this.setState({
      selectedChoice: choiceId
    })
  }

  isChecked (choice) {
    return (this.state.selectedChoice === choice)
  }

  getClassNameInput (choice) {
    if (this.isChecked(choice)) {
      return 'btn btn--light switch--btn u-z-index-1 active'
    }
    return 'btn btn--light switch--btn'
  }

  render () {
    return (
      <fieldset className={'filter-bar__menu-radio-' + this.props.filterId} role="group" aria-labelledby={this.props.filterId}>
        <legend><h2 id={this.props.filterId} className="u-no-margin">{this.props.question}</h2></legend>
        <div className="btn-group">
          <div key={this.props.filterId + 'all'} className={this.getClassNameInput(-1)}>
            <input
              id={'id_choice-' + this.props.filterId + '-all'}
              type="radio"
              value="-1"
              name={this.props.filterId + '-' + allStr}
              className="radio__input"
              checked={this.isChecked(-1)}
              onChange={this.handleOnChange.bind(this)}
            />
            <label
              htmlFor={'id_choice-' + this.props.filterId + '-all'}
            >
              <span>{allStr}</span>
            </label>
          </div>
          {this.props.choiceNames.map((choice, i) => {
            return (
              <div key={this.props.filterId + i} className={this.getClassNameInput(i)}>
                <input
                  id={'id_choice-' + this.props.filterId + '-' + i}
                  type="radio"
                  value={i}
                  name={choice}
                  className="radio__input"
                  checked={this.isChecked(i)}
                  onChange={this.handleOnChange.bind(this)}
                />
                <label
                  htmlFor={'id_choice-' + this.props.filterId + '-' + i}
                >
                  <span>{choice}</span>
                </label>
              </div>
            )
          })}
        </div>
      </fieldset>
    )
  }
}

module.exports = FilterRadio
