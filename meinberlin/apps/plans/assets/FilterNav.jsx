/* global django */
var FilterOptions = require('./FilterOptions')
var FilterButton = require('./FilterButton')
var FilterSecondary = require('./FilterSecondary')
const React = require('react')

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
      isExpanded: isExpanded
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
      isExpanded: isExpanded
    })
  }

  showSecondaryFilters () {
    let isExpanded = !this.state.isExpanded
    if (this.state.displayDistrictOptions || this.state.displayTopicOptions) {
      isExpanded = true
    }
    this.setState({
      displayDistrictOptions: false,
      displayTopicOptions: false,
      displaySecondaryFilters: !this.state.displaySecondaryFilters,
      isExpanded: isExpanded
    })
  }

  clickDistrict (event) {
    let district = event.currentTarget.value
    this.props.selectDistrict(district)
    this.setState({
      displayDistrictOptions: false,
      isExpanded: false
    })
  }

  clickTopic (event) {
    let topic = event.currentTarget.value
    this.props.selectTopic(topic)
    this.setState({
      displayTopicOptions: false,
      isExpanded: false
    })
  }

  getDistrictFilterName () {
    if (this.props.district === '-1') {
      return django.gettext('all')
    }
    return this.props.district
  }

  getTopicFilterName () {
    if (this.props.topic === '-1') {
      return django.gettext('all')
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

  getButtonText (filterType, filterName) {
    return filterType + ': ' + filterName
  }

  render () {
    if (this.props.isStacked) {
      return (
        <div className={this.getFilterBarClassName('--stacked')} role="group" aria-label={django.gettext('Filter bar')}>
          <span className="">{django.gettext('I am interested in projects from')}</span>
          {this.props.district === '-1'
            ? <FilterButton
              className="btn btn--none filter-bar__btn filter-bar__btn--wide filter-bar__btn--unselected"
              ariaExpanded={this.state.displayDistrictOptions}
              showOptions={this.showDistrictOptions.bind(this)}
              id="id_filter_district"
              buttonText={this.getButtonText(django.gettext('District'), this.getDistrictFilterName())}
              iClassName="fa fa-chevron-down"
            />
            : <FilterButton
              className="btn btn--none filter-bar__btn filter-bar__btn--wide filter-bar__btn--selected"
              ariaExpanded={this.state.displayDistrictOptions}
              showOptions={this.showDistrictOptions.bind(this)}
              id="id_filter_district"
              buttonText={this.getDistrictFilterName()}
              iClassName="fa fa-times"
            />
          }
          { this.state.displayDistrictOptions &&
            <FilterOptions
              question={django.gettext('Which district are you interested in?')}
              options={this.props.districtnames}
              onSelect={this.clickDistrict.bind(this)}
              ariaLabelledby="id_filter_district"
              isStacked={this.props.isStacked}
              numColumns={this.props.numColumns}
              hasNoneValue
              selectedChoice={this.props.district}
            />
          }
          {this.props.topic === '-1'
            ? <FilterButton
              className="btn btn--none filter-bar__btn filter-bar__btn--wide filter-bar__btn--unselected"
              ariaExpanded={this.state.displayTopicOptions}
              showOptions={this.showTopicOptions.bind(this)}
              id="id_filter_topic"
              buttonText={this.getButtonText(django.gettext('Topic'), this.getTopicFilterName())}
              iClassName="fa fa-chevron-down"
            />
            : <FilterButton
              className="btn btn--none filter-bar__btn filter-bar__btn--wide filter-bar__btn--selected"
              ariaExpanded={this.state.displayTopicOptions}
              showOptions={this.showTopicOptions.bind(this)}
              id="id_filter_topic"
              buttonText={this.getTopicFilterName()}
              iClassName="fa fa-times"
            />
          }
          { this.state.displayTopicOptions &&
          <FilterOptions
            question={django.gettext('Which topic are you interested in?')}
            options={this.props.topicChoices}
            onSelect={this.clickTopic.bind(this)}
            ariaLabelledby="id_filter_topic"
            isStacked={this.props.isStacked}
            numColumns={this.props.numColumns}
            hasNoneValue={false}
            selectedChoice={this.props.topic}
          />
          }
          { this.props.linkUrl &&
            <div>
              <a
                href={this.props.linkUrl}
                className="u-spacer-top btn btn--small btn--primary btn--full filter-bar__btn--light-homepage">{django.gettext('display projects')}
              </a>
            </div>
          }
          { !this.props.linkUrl &&
            <button
              onClick={this.showSecondaryFilters.bind(this)}
              className="u-spacer-top btn btn--small btn--transparent btn--full filter-bar__btn--light"
              aria-haspopup="true"
              aria-expanded={this.state.displaySecondaryFilters}>
              {django.gettext('more filters')}
            </button>
          }
          { this.state.displaySecondaryFilters &&
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
          }
        </div>
      )
    } else {
      return (
        <div className="filter-bar-container">
          <div className={this.getFilterBarClassName('--horizontal')} role="group" aria-label={django.gettext('Filter bar')}>
            <span className="filter-bar__project-text">{django.gettext('I am interested in projects from')}</span>
            <div className="filter-bar__dropdown">
              {this.props.district === '-1'
                ? <FilterButton
                  className="btn btn--none filter-bar__btn filter-bar__btn--truncate filter-bar__btn--unselected"
                  ariaExpanded={this.state.displayDistrictOptions}
                  showOptions={this.showDistrictOptions.bind(this)}
                  id="id_filter_district"
                  buttonText={this.getButtonText(django.gettext('District'), this.getDistrictFilterName())}
                  iClassName="fa fa-chevron-down"
                />
                : <FilterButton
                  className="btn btn--none filter-bar__btn filter-bar__btn--truncate filter-bar__btn--selected"
                  ariaExpanded={this.state.displayDistrictOptions}
                  showOptions={this.showDistrictOptions.bind(this)}
                  id="id_filter_district"
                  buttonText={this.getDistrictFilterName()}
                  iClassName="fa fa-times"
                />
              }
              { this.state.displayDistrictOptions &&
              <FilterOptions
                question={django.gettext('Which district are you interested in?')}
                options={this.props.districtnames}
                onSelect={this.clickDistrict.bind(this)}
                ariaLabelledby="id_filter_district"
                isStacked={this.props.isStacked}
                numColumns={this.props.numColumns}
                hasNoneValue
                selectedChoice={this.props.district}
              />
              }
            </div>
            <span className="u-md-down-display-none">{django.gettext(' in the area of ')}</span>
            <div className="filter-bar__dropdown">
              {this.props.topic === '-1'
                ? <FilterButton
                  className="btn btn--none filter-bar__btn filter-bar__btn--truncate filter-bar__btn--unselected"
                  ariaExpanded={this.state.displayTopicOptions}
                  showOptions={this.showTopicOptions.bind(this)}
                  id="id_filter_topic"
                  buttonText={this.getButtonText(django.gettext('Topic'), this.getTopicFilterName())}
                  iClassName="fa fa-chevron-down"
                />
                : <FilterButton
                  className="btn btn--none filter-bar__btn filter-bar__btn--truncate filter-bar__btn--selected"
                  ariaExpanded={this.state.displayTopicOptions}
                  showOptions={this.showTopicOptions.bind(this)}
                  id="id_filter_topic"
                  buttonText={this.getTopicFilterName()}
                  iClassName="fa fa-times"
                />
              }
              { this.state.displayTopicOptions &&
              <FilterOptions
                question={django.gettext('Which topic are you interested in?')}
                options={this.props.topicChoices}
                onSelect={this.clickTopic.bind(this)}
                ariaLabelledby="id_filter_topic"
                isStacked={this.props.isStacked}
                numColumns={this.props.numColumns}
                hasNoneValue={false}
                selectedChoice={this.props.topic}
              />
              }
            </div>
            { this.props.linkUrl &&
              <div>
                <a
                  href={this.props.linkUrl}
                  className="btn btn--small btn--primary filter-bar__btn--light-homepage">{django.gettext('display projects')}
                </a>
              </div>
            }
            { (!this.props.linkUrl && this.props.isTablet) &&
              <div>
                <button
                  onClick={this.showSecondaryFilters.bind(this)}
                  className="btn btn--small btn--transparent filter-bar__btn--light"
                  aria-haspopup="true"
                  aria-expanded={this.state.displaySecondaryFilters}>
                  <i className="fas fa-sliders-h" aria-label={django.gettext('more filters')} />
                </button>
              </div>
            }
            { (!this.props.linkUrl && !this.props.isTablet) &&
              <div>
                <button
                  onClick={this.showSecondaryFilters.bind(this)}
                  className="btn btn--small btn--transparent filter-bar__btn--light"
                  aria-haspopup="true"
                  aria-expanded={this.state.displaySecondaryFilters}>
                  {django.gettext('more filters')}
                </button>
              </div>
            }
          </div>
          { this.state.displaySecondaryFilters &&
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
          }
        </div>
      )
    }
  }
}

module.exports = FilterNav
