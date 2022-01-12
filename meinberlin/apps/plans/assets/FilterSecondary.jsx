/* global django */
const Typeahead = require('react-bootstrap-typeahead').Typeahead
const FilterRadio = require('./FilterRadio')
const React = require('react')

const searchTitleStr = django.gettext('Search title')
const orgaStr = django.gettext('Organisation')
const enterOrgaNameStr = django.gettext('Enter the name of the organisation')
const participationStr = django.gettext('Participation')
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
        <label htmlFor="id-title-search">
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
          </button>
          <span className="visually-hidden">{searchTitleStr}
          </span>
        </label>
        {this.props.organisationFilterOnTop &&
          <div className="form-group">
            <div className="typeahead__input-label">
              <h2 className="u-no-margin">{orgaStr}</h2>
            </div>
            <span className="typeahead__input-group">
              <span className="typeahead__input-group-prepend">
                <span className="typeahead__input-group-text">
                  <i className="fas fa-sort-alpha-down" />
                </span>
              </span>
              <Typeahead
                id="organisation-typeahead-id"
                className=""
                onChange={this.clickOrganisation.bind(this)}
                labelKey="name"
                multiple={false}
                options={this.props.organisations}
                selected={this.state.organisationChoice}
                placeholder={enterOrgaNameStr}
              />
            </span>
          </div>}
        <div className="filter-bar__menu-radio-group">
          <div className="filter-bar__menu-radio-part">
            <FilterRadio
              filterId="par"
              question={participationStr}
              chosen={this.state.participationChoice}
              choiceNames={this.props.participationNames}
              onSelect={this.clickParticipation.bind(this)}
            />
          </div>
          <div className="filter-bar__menu-radio-proj">
            <FilterRadio
              filterId="sta"
              question={projectStatStr}
              chosen={this.state.statusChoice}
              choiceNames={this.props.statusNames}
              onSelect={this.clickStatus.bind(this)}
            />
          </div>
        </div>
        {!this.props.organisationFilterOnTop &&
          <div className="form-group">
            <div className="typeahead__input-label">
              <h2 className="u-no-margin">{orgaStr}</h2>
            </div>
            <span className="typeahead__input-group">
              <span className="typeahead__input-group-prepend">
                <span className="typeahead__input-group-text">
                  <i className="fas fa-sort-alpha-down" />
                </span>
              </span>
              <Typeahead
                id="organisation-typeahead-id"
                className="typeahead__input-group-append"
                onChange={this.clickOrganisation.bind(this)}
                labelKey="name"
                multiple={false}
                options={this.props.organisations}
                selected={this.state.organisationChoice}
                placeholder={enterOrgaNameStr}
              />
            </span>
          </div>}
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
