/* global django */
var Typeahead = require('react-bootstrap-typeahead').Typeahead
var FilterRadio = require('./FilterRadio')
const React = require('react')

class FilterSecondary extends React.Component {
  constructor (props) {
    super(props)

    let orgChoice = ['']
    if (this.props.organisation !== '-1') {
      orgChoice = [this.props.organisation]
    }

    this.state = {
      participationChoice: this.props.participation,
      statusChoice: this.props.status,
      organisationChoice: orgChoice,
      titleSearch: this.props.titleSearch
    }
  }

  submitSecondaryFilters (e) {
    e.preventDefault()
    this.props.showSecondaryFilters()
    this.props.selectParticipation(this.state.participationChoice)
    this.props.selectStatus(this.state.statusChoice)
    this.props.selectOrganisation(this.state.organisationChoice[0])
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

  clickOrganisation (organisation) {
    this.setState({
      organisationChoice: organisation
    })
  }

  render () {
    return (
      <form className="filter-bar__menu">
        <div className="filter-bar__menu-radio-group">
          <div className="filter-bar__menu-radio-part">
            <FilterRadio
              filterId="par"
              question={django.gettext('Participation')}
              chosen={this.state.participationChoice}
              choiceNames={this.props.participationNames}
              onSelect={this.clickParticipation.bind(this)}
            />
          </div>
          <div className="filter-bar__menu-radio-proj">
            <FilterRadio
              filterId="sta"
              question={django.gettext('Project status')}
              chosen={this.state.statusChoice}
              choiceNames={this.props.statusNames}
              onSelect={this.clickStatus.bind(this)}
            />
          </div>
        </div>
        <Typeahead
          onChange={this.clickOrganisation.bind(this)}
          labelKey="name"
          multiple={false}
          options={this.props.organisations}
          selected={this.state.organisationChoice}
          placeholder={django.gettext('Show Organisation ...')}
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
