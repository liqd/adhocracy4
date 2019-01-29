/* global django */
var FilterRadio = require('./FilterRadio')
const React = require('react')

class FilterSecondary extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      participationChoice: this.props.participation,
      statusChoice: this.props.status,
      organisationChoice: this.props.organisation,
      titleSearch: this.props.titleSearch
    }
  }

  submitSecondaryFilters (e) {
    e.preventDefault()
    this.props.showSecondaryFilters()
    this.props.selectParticipation(this.state.participationChoice)
    this.props.selectStatus(this.state.statusChoice)
    this.props.selectOrganisation(this.state.organisationChoice)
    this.props.selectTitleSearch(this.state.titleSearch)
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
        <FilterRadio
          filterId="par"
          question={django.gettext('Participation')}
          chosen={this.state.participationChoice}
          choiceNames={this.props.participationNames}
          onSelect={this.clickParticipation.bind(this)}
        />
        <FilterRadio
          filterId="sta"
          question={django.gettext('Project status')}
          chosen={this.state.statusChoice}
          choiceNames={this.props.statusNames}
          onSelect={this.clickStatus.bind(this)}
        />
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
