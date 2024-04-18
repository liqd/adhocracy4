/* global django */
const FilterOptions = require('./FilterOptions')
const FilterButton = require('./FilterButton')
const FilterSecondary = require('./FilterSecondary')
const React = require('react')
const allStr = django.gettext('all')
const filterBarStr = django.gettext('Filter bar for Project overview')
const interestedInProjectsStr = django.gettext('I am interested in projects from')
const allDistrictsStr = django.gettext('„ all Districts “')
const whichDistrictsStr = django.gettext('Which district are you interested in?')
const allTopicsStr = django.gettext('„ all Topics “')
const whichTopicStr = django.gettext('Which topic are you interested in?')
const displayProjectsStr = django.gettext('display projects')
const moreFiltersStr = django.gettext('more filters')
const closeStr = django.gettext('Close')
const inAreaStr = django.gettext('in the area of')

class FilterNav extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      displayDistrictOptions: false,
      displayTopicOptions: false,
      displaySecondaryFilters: false,
      isExpanded: false
    }
  }

  showDistrictOptions () {
    let isExpanded = !this.state.isExpanded
    if (this.state.displayTopicOptions || this.state.displaySecondaryFilters) {
      isExpanded = true
    }
    this.setState({
      displayTopicOptions: false,
      displayDistrictOptions: !this.state.displayDistrictOptions,
      displaySecondaryFilters: false,
      isExpanded
    })
  }

  showTopicOptions () {
    let isExpanded = !this.state.isExpanded
    if (this.state.displayDistrictOptions || this.state.displaySecondaryFilters) {
      isExpanded = true
    }
    this.setState({
      displayDistrictOptions: false,
      displayTopicOptions: !this.state.displayTopicOptions,
      displaySecondaryFilters: false,
      isExpanded
    })
  }

  showSecondaryFilters () {
    let isExpanded = !this.state.isExpanded
    if (this.state.displayDistrictOptions || this.state.displayTopicOptions) {
      isExpanded = true
    }
    this.props.updateFilterStatus(isExpanded)
    this.setState({
      displayDistrictOptions: false,
      displayTopicOptions: false,
      displaySecondaryFilters: !this.state.displaySecondaryFilters,
      isExpanded
    })
  }

  closeSecondaryFilters () {
    this.setState({
      displaySecondaryFilters: false,
      isExpanded: false
    })
  }

  clickDistrict (event) {
    const district = event.currentTarget.value
    this.props.selectDistrict(district)
    this.setState({
      displayDistrictOptions: false,
      isExpanded: false
    })
  }

  clickTopic (event) {
    const topic = event.currentTarget.value
    this.props.selectTopic(topic)
    this.setState({
      displayTopicOptions: false,
      isExpanded: false
    })
  }

  closeFilters () {
    this.setState({
      displayTopicOptions: false,
      displayDistrictOptions: false,
      displaySecondaryFilters: false,
      isExpanded: false
    })
  }

  getDistrictFilterName () {
    if (this.props.district === '-1') {
      return allStr
    }
    return this.props.district
  }

  getTopicFilterName () {
    if (this.props.topic === '-1') {
      return allStr
    }
    return this.props.topicChoices[this.props.topic]
  }

  getFilterBarClassName (variant) {
    if (this.state.isExpanded) {
      return 'filter-bar--open filter-bar filter-bar' + variant
    } else {
      return 'filter-bar filter-bar' + variant
    }
  }

  getSelectedTopicOption (choice) {
    if (choice === '-1') {
      return choice
    }
    return this.props.topicChoices[this.props.topic]
  }

  render () {
    if (this.props.isStacked) {
      return (
        <div>
          <div className={this.getFilterBarClassName('--stacked')} role="group" aria-label={filterBarStr}>
            <span>{interestedInProjectsStr}</span>
            {this.props.district === '-1'
              ? (
                <FilterButton
                  className="btn filter-bar__btn filter-bar__btn--wide filter-bar__btn--unselected"
                  ariaExpanded={this.state.displayDistrictOptions}
                  showOptions={this.showDistrictOptions.bind(this)}
                  id="id_filter_district"
                  buttonText={allDistrictsStr}
                  iClassName="fa fa-chevron-down"
                />
                )
              : (
                <FilterButton
                  className="btn filter-bar__btn filter-bar__btn--wide filter-bar__btn--selected"
                  ariaExpanded={this.state.displayDistrictOptions}
                  showOptions={this.showDistrictOptions.bind(this)}
                  id="id_filter_district"
                  buttonText={this.getDistrictFilterName()}
                  iClassName="fa fa-chevron-down"
                />
                )}
            {this.state.displayDistrictOptions &&
              <FilterOptions
                question={whichDistrictsStr}
                options={this.props.districtnames}
                onSelect={this.clickDistrict.bind(this)}
                ariaLabelledby="id_filter_district"
                isStacked={this.props.isStacked}
                numColumns={this.props.numColumns}
                hasNoneValue
                selectedChoice={this.props.district}
              />}
            {this.props.topic === '-1'
              ? (
                <FilterButton
                  className="btn filter-bar__btn filter-bar__btn--wide filter-bar__btn--unselected"
                  ariaExpanded={this.state.displayTopicOptions}
                  showOptions={this.showTopicOptions.bind(this)}
                  id="id_filter_topic"
                  buttonText={allTopicsStr}
                  iClassName="fa fa-chevron-down"
                />
                )
              : (
                <FilterButton
                  className="btn filter-bar__btn filter-bar__btn--wide filter-bar__btn--selected"
                  ariaExpanded={this.state.displayTopicOptions}
                  showOptions={this.showTopicOptions.bind(this)}
                  id="id_filter_topic"
                  buttonText={this.getTopicFilterName()}
                  iClassName="fa fa-chevron-down"
                />
                )}
            {this.state.displayTopicOptions &&
              <FilterOptions
                question={whichTopicStr}
                options={this.props.topicChoices}
                onSelect={this.clickTopic.bind(this)}
                ariaLabelledby="id_filter_topic"
                isStacked={this.props.isStacked}
                numColumns={this.props.numColumns}
                hasNoneValue={false}
                selectedChoice={this.getSelectedTopicOption(this.props.topic)}
              />}
            {this.props.linkUrl &&
              <div>
                <a
                  href={this.props.linkUrl}
                  className="u-spacer-top btn btn--small btn--primary btn--full u-spacer-bottom filter-bar__btn--light-homepage"
                >{displayProjectsStr}
                </a>
              </div>}
            {!this.props.linkUrl &&
              <button
                onClick={this.showSecondaryFilters.bind(this)}
                className="u-spacer-top btn btn--small btn--full u-spacer-bottom filter-bar__btn--light"
                aria-haspopup="true"
                aria-expanded={this.state.displaySecondaryFilters}
              >
                {moreFiltersStr}
              </button>}
            {this.state.displaySecondaryFilters &&
              <div className="modal filter-secondary__modal" id="filter-modal" role="dialog">
                <div className="modal-dialog modal-lg" role="document">
                  <div className="modal-content filter-secondary__modal-content">
                    <div className="modal-header filter-secondary__modal-header"><button type="button" className="close" onClick={this.closeSecondaryFilters.bind(this)} aria-label={closeStr}><i className="fa fa-times" /></button></div>
                    <div className="modal-body">
                      <FilterSecondary
                        selectParticipation={this.props.selectParticipation.bind(this)}
                        selectStatus={this.props.selectStatus.bind(this)}
                        selectOrganisation={this.props.selectOrganisation.bind(this)}
                        selectTitleSearch={this.props.selectTitleSearch.bind(this)}
                        showSecondaryFilters={this.showSecondaryFilters.bind(this)}
                        participation={this.props.participation}
                        participationNames={this.props.participationNames}
                        status={this.props.status}
                        statusNames={this.props.statusNames}
                        organisation={this.props.organisation}
                        organisations={this.props.organisations}
                        numColumns={this.props.numColumns}
                        titleSearch={this.props.titleSearch}
                      />
                    </div>
                  </div>
                </div>
              </div>}
          </div>
          <div className="outer-handler" onClick={() => this.closeFilters()} role="none" />
        </div>
      )
    } else {
      return (
        <div className="l-frame filter-bar-container">
          <div className={this.getFilterBarClassName('--horizontal')} role="group" aria-label={filterBarStr}>
            <span className="filter-bar__project-text">{interestedInProjectsStr}</span>
            <div className="filter-bar__dropdown">
              {this.props.district === '-1'
                ? (
                  <FilterButton
                    className="btn filter-bar__btn filter-bar__btn--truncate filter-bar__btn--unselected"
                    ariaExpanded={this.state.displayDistrictOptions}
                    showOptions={this.showDistrictOptions.bind(this)}
                    id="id_filter_district"
                    buttonText={allDistrictsStr}
                    iClassName="fa fa-chevron-down"
                  />
                  )
                : (
                  <FilterButton
                    className="btn filter-bar__btn filter-bar__btn--truncate filter-bar__btn--selected"
                    ariaExpanded={this.state.displayDistrictOptions}
                    showOptions={this.showDistrictOptions.bind(this)}
                    id="id_filter_district"
                    buttonText={this.getDistrictFilterName()}
                    iClassName="fa fa-chevron-down"
                  />
                  )}
              {this.state.displayDistrictOptions &&
                <FilterOptions
                  question={whichDistrictsStr}
                  options={this.props.districtnames}
                  onSelect={this.clickDistrict.bind(this)}
                  ariaLabelledby="id_filter_district"
                  isStacked={this.props.isStacked}
                  numColumns={this.props.numColumns}
                  hasNoneValue
                  selectedChoice={this.props.district}
                />}
            </div>
            <span className="u-md-down-display-none">{inAreaStr}</span>
            <div className="filter-bar__dropdown">
              {this.props.topic === '-1'
                ? (
                  <FilterButton
                    className="btn filter-bar__btn filter-bar__btn--truncate filter-bar__btn--unselected"
                    ariaExpanded={this.state.displayTopicOptions}
                    showOptions={this.showTopicOptions.bind(this)}
                    id="id_filter_topic"
                    buttonText={allTopicsStr}
                    iClassName="fa fa-chevron-down"
                  />
                  )
                : (
                  <FilterButton
                    className="btn filter-bar__btn filter-bar__btn--truncate filter-bar__btn--selected"
                    ariaExpanded={this.state.displayTopicOptions}
                    showOptions={this.showTopicOptions.bind(this)}
                    id="id_filter_topic"
                    buttonText={this.getTopicFilterName()}
                    iClassName="fa fa-chevron-down"
                  />
                  )}
              {this.state.displayTopicOptions &&
                <FilterOptions
                  question={whichTopicStr}
                  options={this.props.topicChoices}
                  onSelect={this.clickTopic.bind(this)}
                  ariaLabelledby="id_filter_topic"
                  isStacked={this.props.isStacked}
                  numColumns={this.props.numColumns}
                  hasNoneValue={false}
                  selectedChoice={this.getSelectedTopicOption(this.props.topic)}
                />}
            </div>
            <span className="u-md-down-display-none">.</span>
            {this.props.linkUrl &&
              <div>
                <a
                  href={this.props.linkUrl}
                  className="btn btn--small btn--primary filter-bar__btn--light-homepage"
                >{displayProjectsStr}
                </a>
              </div>}
            {(!this.props.linkUrl && this.props.isTablet) &&
              <div>
                <button
                  onClick={this.showSecondaryFilters.bind(this)}
                  className="btn btn--small filter-bar__btn--light"
                  aria-haspopup="true"
                  aria-expanded={this.state.displaySecondaryFilters}
                >
                  <i className="fas fa-sliders-h" aria-label={moreFiltersStr} />
                </button>
              </div>}
            {(!this.props.linkUrl && !this.props.isTablet) &&
              <div>
                <button
                  onClick={this.showSecondaryFilters.bind(this)}
                  className="btn btn--small filter-bar__btn--light"
                  aria-haspopup="true"
                  aria-expanded={this.state.displaySecondaryFilters}
                >
                  {moreFiltersStr}
                </button>
              </div>}
          </div>
          {this.state.displaySecondaryFilters &&
            <FilterSecondary
              selectParticipation={this.props.selectParticipation.bind(this)}
              selectStatus={this.props.selectStatus.bind(this)}
              selectOrganisation={this.props.selectOrganisation.bind(this)}
              selectTitleSearch={this.props.selectTitleSearch.bind(this)}
              showSecondaryFilters={this.showSecondaryFilters.bind(this)}
              participation={this.props.participation}
              participationNames={this.props.participationNames}
              status={this.props.status}
              statusNames={this.props.statusNames}
              organisation={this.props.organisation}
              organisations={this.props.organisations}
              numColumns={this.props.numColumns}
              titleSearch={this.props.titleSearch}
            />}
          <div className="outer-handler" onClick={() => this.closeFilters()} role="none" />
        </div>
      )
    }
  }
}

module.exports = FilterNav
