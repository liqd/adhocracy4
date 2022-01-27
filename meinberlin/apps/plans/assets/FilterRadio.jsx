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
      <fieldset className="u-no-border u-no-margin u-no-padding">
        <legend><h2 className="u-no-margin">{this.props.question}</h2></legend>
        <div className="btn-group " role="group">
          <label
            className={this.getClassNameInput(-1)}
            key={this.props.filterId + 'all'}
            htmlFor={'id_choice-' + this.props.filterId + '-all'}
          >
            <input
              className="radio__input"
              type="radio"
              id={'id_choice-' + this.props.filterId + '-all'}
              value="-1"
              checked={this.isChecked(-1)}
              onChange={this.handleOnChange.bind(this)}
            />
            <span>{allStr}</span>
          </label>
          {this.props.choiceNames.map((choice, i) => {
            return (
              <label
                className={this.getClassNameInput(i)}
                key={this.props.filterId + i}
                htmlFor={'id_choice-' + this.props.filterId + '-' + i}
              >
                <input
                  className="radio__input"
                  type="radio"
                  id={'id_choice-' + this.props.filterId + '-' + i}
                  value={i}
                  checked={this.isChecked(i)}
                  onChange={this.handleOnChange.bind(this)}
                />
                <span>{choice}</span>
              </label>
            )
          })}
        </div>
      </fieldset>
    )
  }
}

module.exports = FilterRadio
