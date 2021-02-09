/* global django */
const Typeahead = require('react-bootstrap-typeahead').Typeahead
const FilterRadio = require('./FilterRadio')
const React = require('react')

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
            placeholder={django.gettext('Search title')}
            value={this.state.titleSearchChoice}
            onChange={this.changeTitleSearch.bind(this)}
          />
          <button
            className="input-group__after btn btn--light filter-bar__search--btn"
            type="submit"
            onClick={this.submitSecondaryFilters.bind(this)}
          >
            <i className="fa fa-search" aria-hidden="true" />
          </button>
          <span className="sr-only">{django.gettext('Search title')}
          </span>
        </label>
        {this.props.organisationFilterOnTop &&
          <div className="form-group">
            <div className="typeahead__input-label">
              <h2 className="u-no-margin">{django.gettext('Organisation')}</h2>
            </div>
            <span className="typeahead__input-group">
              <span className="typeahead__input-group-prepend">
                <span className="typeahead__input-group-text">
                  <i className="fas fa-sort-alpha-down" />
                </span>
              </span>
              <Typeahead
                id="organisation-typeahead-id"
                className="input-group__input"
                onChange={this.clickOrganisation.bind(this)}
                labelKey="name"
                multiple={false}
                options={this.props.organisations}
                selected={this.state.organisationChoice}
                placeholder={django.gettext('Enter the name of the organisation')}
              />
            </span>
          </div>}
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
        {!this.props.organisationFilterOnTop &&
          <div className="form-group">
            <div className="typeahead__input-label">
              <h2 className="u-no-margin">{django.gettext('Organisation')}</h2>
            </div>
            <span className="typeahead__input-group">
              <span className="typeahead__input-group-prepend">
                <span className="typeahead__input-group-text">
                  <i className="fas fa-sort-alpha-down" />
                </span>
              </span>
              <Typeahead
                id="organisation-typeahead-id"
                className="input-group__input"
                onChange={this.clickOrganisation.bind(this)}
                labelKey="name"
                multiple={false}
                options={this.props.organisations}
                selected={this.state.organisationChoice}
                placeholder={django.gettext('Enter the name of the organisation')}
              />
            </span>
          </div>}
        <button
          className="btn btn--primary filter-secondary__btn"
          type="submit"
          onClick={this.submitSecondaryFilters.bind(this)}
        >
          {django.gettext('show projects')}
        </button>
      </form>
    )
  }
}

module.exports = FilterSecondary
