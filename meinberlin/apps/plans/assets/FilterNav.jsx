/* global django */
var FilterOptions = require('./FilterOptions')
var FilterButton = require('./FilterButton')
const React = require('react')

class FilterNav extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      displayDistrictOptions: false,
      displayTopicOptions: false,
      isExpanded: false
    }
  }

  showDistrictOptions () {
    let isExpanded = !this.state.isExpanded
    if (this.state.displayTopicOptions) {
      isExpanded = true
    }
    this.setState({
      displayTopicOptions: false,
      displayDistrictOptions: !this.state.displayDistrictOptions,
      isExpanded: isExpanded
    })
  }

  showTopicOptions () {
    let isExpanded = !this.state.isExpanded
    if (this.state.displayDistrictOptions) {
      isExpanded = true
    }
    this.setState({
      displayDistrictOptions: false,
      displayTopicOptions: !this.state.displayTopicOptions,
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

  getAriaExpanded (displayOptions) {
    if (this.state.isExpanded & displayOptions) {
      return true
    }
    return false
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
              ariaExpanded={this.getAriaExpanded(this.state.displayDistrictOptions)}
              showOptions={this.showDistrictOptions.bind(this)}
              id="id_filter_district"
              buttonText={this.getButtonText(django.gettext('District'), this.getDistrictFilterName())}
              iClassName="fa fa-chevron-down"
            />
            : <FilterButton
              className="btn btn--none filter-bar__btn filter-bar__btn--wide filter-bar__btn--selected"
              ariaExpanded={this.getAriaExpanded(this.state.displayDistrictOptions)}
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
            />
          }
          {this.props.topic === '-1'
            ? <FilterButton
              className="btn btn--none filter-bar__btn filter-bar__btn--wide filter-bar__btn--unselected"
              ariaExpanded={this.getAriaExpanded(this.state.displayTopicOptions)}
              showOptions={this.showTopicOptions.bind(this)}
              id="id_filter_topic"
              buttonText={this.getButtonText(django.gettext('Topic'), this.getTopicFilterName())}
              iClassName="fa fa-chevron-down"
            />
            : <FilterButton
              className="btn btn--none filter-bar__btn filter-bar__btn--wide filter-bar__btn--selected"
              ariaExpanded={this.getAriaExpanded(this.state.displayTopicOptions)}
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
          />
          }
        </div>
      )
    } else {
      return (
        <div className="filter-bar-container">
          <div className={this.getFilterBarClassName('--horizontal')} role="group" aria-label={django.gettext('Filter bar')}>
            <span>{django.gettext('I am interested in projects from')}</span>
            <div className="filter-bar__dropdown">
              {this.props.district === '-1'
                ? <FilterButton
                  className="btn btn--none filter-bar__btn filter-bar__btn--truncate filter-bar__btn--unselected"
                  ariaExpanded={this.getAriaExpanded(this.state.displayDistrictOptions)}
                  showOptions={this.showDistrictOptions.bind(this)}
                  id="id_filter_district"
                  buttonText={this.getButtonText(django.gettext('District'), this.getDistrictFilterName())}
                  iClassName="fa fa-chevron-down"
                />
                : <FilterButton
                  className="btn btn--none filter-bar__btn filter-bar__btn--truncate filter-bar__btn--selected"
                  ariaExpanded={this.getAriaExpanded(this.state.displayDistrictOptions)}
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
              />
              }
            </div>
            <span>{django.gettext(' in the area of ')}</span>
            <div className="filter-bar__dropdown">
              {this.props.topic === '-1'
                ? <FilterButton
                  className="btn btn--none filter-bar__btn filter-bar__btn--truncate filter-bar__btn--unselected"
                  ariaExpanded={this.getAriaExpanded(this.state.displayTopicOptions)}
                  showOptions={this.showTopicOptions.bind(this)}
                  id="id_filter_topic"
                  buttonText={this.getButtonText(django.gettext('Topic'), this.getTopicFilterName())}
                  iClassName="fa fa-chevron-down"
                />
                : <FilterButton
                  className="btn btn--none filter-bar__btn filter-bar__btn--truncate filter-bar__btn--selected"
                  ariaExpanded={this.getAriaExpanded(this.state.displayTopicOptions)}
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
              />
              }
            </div>
            <div>
              <button
                className="btn btn--small btn--transparent filter-bar__btn--light">{django.gettext('more filters')}</button>
            </div>
          </div>
        </div>
      )
    }
  }
}

module.exports = FilterNav
