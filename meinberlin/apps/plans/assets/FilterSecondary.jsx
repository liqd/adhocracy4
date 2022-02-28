/* global django */
import React from 'react'
import { TypeaheadField } from '../../contrib/assets/TypeaheadField'
const FilterRadio = require('./FilterRadio')

const searchTitleStr = django.gettext('Search title')
const performSearchStr = django.gettext('Perform search')
const orgaStr = django.gettext('Organisation')
const enterOrgaNameStr = django.gettext('Enter the name of the organisation')
const participationStr = django.gettext('Level of participation')
const projectStatStr = django.gettext('Project status')
const showProjectsStr = django.gettext('show projects')

class FilterSecondary extends React.Component {
  constructor (props) {
    super(props)

    let titleSearchChoice = this.props.titleSearch
    if (titleSearchChoice === '-1') {
      titleSearchChoice = ''
    }

    let orgChoice = null
    if (this.props.organisation !== '-1') {
      orgChoice = [this.props.organisation]
    }

    this.state = {
      participationChoice: this.props.participation,
      statusChoice: this.props.status,
      organisationChoice: orgChoice,
      titleSearchChoice: titleSearchChoice
    }
  }

  submitSecondaryFilters (e) {
    e.preventDefault()

    let titleSearchChoice = this.state.titleSearchChoice
    if (titleSearchChoice === '') {
      titleSearchChoice = '-1'
    }

    let organisationChoice = '-1'
    if (this.state.organisationChoice !== null && this.state.organisationChoice !== '') {
      organisationChoice = this.state.organisationChoice[0]
    }

    this.props.showSecondaryFilters()
    this.props.selectParticipation(this.state.participationChoice)
    this.props.selectStatus(this.state.statusChoice)
    this.props.selectOrganisation(organisationChoice)
    this.props.selectTitleSearch(titleSearchChoice)
  }

  changeTitleSearch (e) {
    const value = e.currentTarget.value
    this.setState({
      titleSearchChoice: value
    })
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
        <div role="search">
          <label htmlFor="id-title-search"><span className="visually-hidden">{searchTitleStr}</span></label>
          <input
            className="input-group__input filter-bar__search"
            type="text"
            id="id-title-search"
            placeholder={searchTitleStr}
            value={this.state.titleSearchChoice}
            onChange={this.changeTitleSearch.bind(this)}
          />
          <button
            className="input-group__after input-group__after--search btn btn--light"
            type="submit"
            onClick={this.submitSecondaryFilters.bind(this)}
          >
            <i className="fa fa-search" aria-hidden="true" />
            <span className="visually-hidden">{performSearchStr}</span>
          </button>

        </div>
        <FilterRadio
          filterId="par"
          question={participationStr}
          chosen={this.state.participationChoice}
          choiceNames={this.props.participationNames}
          onSelect={this.clickParticipation.bind(this)}
        />
        <div className="filter-bar__section">
          <FilterRadio
            filterId="sta"
            question={projectStatStr}
            chosen={this.state.statusChoice}
            choiceNames={this.props.statusNames}
            onSelect={this.clickStatus.bind(this)}
          />
          <TypeaheadField
            typeaheadHeading={orgaStr}
            uniqueId="organisation-typeahead-id"
            onTypeaheadChange={this.clickOrganisation.bind(this)}
            typeaheadOptions={this.props.organisations}
            typeaheadSelected={this.state.organisationChoice}
            typeaheadPlaceholder={enterOrgaNameStr}
            multipleBoolean={false}
          />
        </div>
        <button
          className="btn btn--primary filter-secondary__btn"
          type="submit"
          onClick={this.submitSecondaryFilters.bind(this)}
        >
          {showProjectsStr}
        </button>
      </form>
    )
  }
}

module.exports = FilterSecondary
