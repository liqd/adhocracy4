/* global django */
var FilterRadio = require('./FilterRadio')
const React = require('react')

class FilterSecondary extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      participationChoice: this.props.participation,
      statusChoice: this.props.status
    }
  }

  submitSecondaryFilters (e) {
    e.preventDefault()
    this.props.showSecondaryFilters()
    this.props.selectParticipation(this.state.participationChoice)
    this.props.selectStatus(this.state.statusChoice)
  }

  clickParticipation (participation) {
    this.setState({
      participationChoice: participation
    })
  }

  clickStatus (status) {
    this.setState({
      statusChoice: status
    })
  }

  render () {
    return (
      <form className="filter-bar__menu">
        <div className="filter-bar__menu-radio-group">
          <div className="filter-bar__menu-radio-1">
            <FilterRadio
              filterId="par"
              question={django.gettext('Participation')}
              chosen={this.state.participationChoice}
              choiceNames={this.props.participationNames}
              onSelect={this.clickParticipation.bind(this)}
            />
          </div>
          <div className="filter-bar__menu-radio-2">
            <FilterRadio
              filterId="sta"
              question={django.gettext('Project status')}
              chosen={this.state.statusChoice}
              choiceNames={this.props.statusNames}
              onSelect={this.clickStatus.bind(this)}
            />
          </div>
        </div>
        <button
          className="btn btn-primary"
          type="submit"
          onClick={this.submitSecondaryFilters.bind(this)}>
          {django.gettext('show projects')}
        </button>
      </form>
    )
  }
}

module.exports = FilterSecondary
