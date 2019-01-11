/* global django */
var FilterOptions = require('./FilterOptions')
var FilterAccordeon = require('./FilterAccordeon')
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
    let isExpanded = !!this.state.isExpanded
    this.setState({
      displayTopicOptions: false,
      displayDistrictOptions: !this.state.displayDistrictOptions,
      isExpanded: isExpanded
    })
  }

  showTopicOptions () {
    let isExpanded = !!this.state.isExpanded
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

  toggleIsExpanded () {
    this.setState({
      isExpanded: !this.state.isExpanded
    })
  }

  getAriaExpanded (displayOptions) {
    if (this.state.isExpanded & displayOptions) {
      return true
    }
    return false
  }

  render () {
    if (this.props.isStacked) {
      return (
        <div className={this.getFilterBarClassName('--stacked')} role="group" aria-label={django.gettext('Filter bar')}>
          <span className="">{django.gettext('I am interested in projects from')}</span>
          <FilterAccordeon
            titlePrefix={django.gettext('District')}
            title={this.getDistrictFilterName()}
            question={django.gettext('Which district are you interested in?')}
            identifier={'district'}
            options={this.props.districtnames}
            onSelect={this.clickDistrict.bind(this)}
            updateIsExpanded={this.toggleIsExpanded.bind(this)}
          />
          <FilterAccordeon
            titlePrefix={django.gettext('Topic')}
            title={this.getTopicFilterName()}
            question={django.gettext('Which topic are you interested in?')}
            identifier={'topic'}
            options={this.props.topicChoices}
            onSelect={this.clickTopic.bind(this)}
            updateIsExpanded={this.toggleIsExpanded.bind(this)}
          />
        </div>
      )
    } else {
      return (
        <div className="filter-bar-container">
          <div className={this.getFilterBarClassName('--horizontal')} role="group" aria-label={django.gettext('Filter bar')}>
            <span>{django.gettext('I am interested in projects from')}</span>
            <div className="filter-bar__dropdown">
              {this.props.district === '-1'
                ? <button type="button"
                  className="btn btn--none filter-bar__btn filter-bar__btn--truncate filter-bar__btn--unselected"
                  data-flip="false"
                  aria-haspopup="true"
                  aria-expanded={this.getAriaExpanded(this.state.displayDistrictOptions)}
                  onClick={this.showDistrictOptions.bind(this)}
                  id="id_filter_district">
                  {django.gettext('District')}: {this.getDistrictFilterName()}
                  <i className="fa fa-chevron-down" aria-hidden="true" />
                </button>
                : <button type="button"
                  className="btn btn--none filter-bar__btn filter-bar__btn--truncate filter-bar__btn--selected"
                  data-flip="false"
                  aria-haspopup="true"
                  aria-expanded={this.getAriaExpanded(this.state.displayDistrictOptions)}
                  onClick={this.showDistrictOptions.bind(this)}
                  id="id_filter_district">
                  {this.getDistrictFilterName()}
                  <i className="fa fa-times" aria-hidden="true" />
                </button>
              }
              { this.state.displayDistrictOptions &&
              <FilterOptions
                question={django.gettext('Which district are you interested in?')}
                options={this.props.districtnames}
                onSelect={this.clickDistrict.bind(this)}
                ariaLabelledby="id_filter_district"
              />
              }
            </div>
            <span>{django.gettext(' in the area of ')}</span>
            <div className="filter-bar__dropdown">
              {this.props.topic === '-1'
                ? <button type="button"
                  className="btn btn--none filter-bar__btn filter-bar__btn--truncate filter-bar__btn--unselected"
                  data-flip="false"
                  aria-haspopup="true"
                  aria-expanded={this.getAriaExpanded(this.state.displayTopicOptions)}
                  onClick={this.showTopicOptions.bind(this)}
                  id="id_filter_topic">
                  {django.gettext('Topic')}: {this.getTopicFilterName()}
                  <i className="fa fa-chevron-down" aria-hidden="true" />
                </button>
                : <button type="button"
                  className="btn btn--none filter-bar__btn filter-bar__btn--truncate filter-bar__btn--selected"
                  data-flip="false"
                  aria-haspopup="true"
                  aria-expanded={this.getAriaExpanded(this.state.displayTopicOptions)}
                  onClick={this.showTopicOptions.bind(this)}
                  id="id_filter_topic">
                  {this.getTopicFilterName()}
                  <i className="fa fa-times" aria-hidden="true" />
                </button>
              }
              { this.state.displayTopicOptions &&
              <FilterOptions
                question={django.gettext('Which topic are you interested in?')}
                options={this.props.topicChoices}
                onSelect={this.clickTopic.bind(this)}
                ariaLabelledby="id_filter_topic"
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
