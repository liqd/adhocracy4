/* global django */
var FilterRadio = require('./FilterRadio')
const React = require('react')

class FilterSecondary extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      participationChoice: this.props.participation
    }
  }

  submitSecondaryFilters (e) {
    e.preventDefault()
    this.props.showSecondaryFilters()
    this.props.selectParticipation(this.state.participationChoice)
  }

  clickParticipation (participation) {
    this.setState({
      participationChoice: participation
    })
  }

  render () {
    return (
      <form className="filter-bar__menu">
        <FilterRadio
          filterId="parti"
          question={django.gettext('Participation')}
          chosen={this.state.participationChoice}
          choiceNames={this.props.participationNames}
          onSelect={this.clickParticipation.bind(this)}
        />
        <button
          type="submit"
          onClick={this.submitSecondaryFilters.bind(this)}>
          {django.gettext('show projects')}
        </button>
      </form>
    )
  }
}

module.exports = FilterSecondary
