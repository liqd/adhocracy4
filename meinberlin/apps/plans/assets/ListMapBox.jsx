/* global django */
import StickyBox from 'react-sticky-box'
const React = require('react')
const $ = require('jquery')
let PlansList = require('./PlansList')
let PlansMap = require('./PlansMap')

class ListMapBox extends React.Component {
  constructor (props) {
    super(props)

    let selectedDistrictIdentifier = -1
    if (props.selectedDistrict !== '-1') {
      selectedDistrictIdentifier = props.selectedDistrict
    }

    let selectedTopicIdentifier = -1
    if (props.selectedTopic !== '-1') {
      selectedTopicIdentifier = props.selectedTopic
    }

    this.state = {
      items: [],
      searchResults: null,
      address: null,
      selected: null,
      displayError: false,
      displayResults: false,
      showListMap: true,
      resizeMap: false,
      filters: {
        status: -1,
        participation: -1,
        district: selectedDistrictIdentifier,
        topic: selectedTopicIdentifier
      }
    }
  }

  isInFilter (item) {
    let filters = this.state.filters
    return (filters.topic === -1 || filters.topic === item.topic) &&
      (filters.district === -1 || filters.district === item.district)
  }

  componentDidMount () {
    let items = []
    this.props.items.forEach((item, i) => {
      if (this.isInFilter(item)) {
        items.push(item)
      }
    })
    this.setState({
      items: items
    })
  }

  toggleSwitch () {
    let newValue = !this.state.showListMap
    this.setState({ showListMap: newValue })
  }

  hideMap (e) {
    e.preventDefault()
    $('#map').addClass('u-mobile-display-none')
    $('#list').removeClass('u-mobile-display-none')
  }

  hideList (e) {
    e.preventDefault()
    $('#list').addClass('u-mobile-display-none')
    $('#map').removeClass('u-mobile-display-none')
    $('#map').css('display', 'block')
    this.setState({ resizeMap: true })
  }

  render () {
    return (
      <div>
        <div>
          <div className="u-spacer-left u-spacer-right">
            <div className="switch-group" role="group" aria-label={django.gettext('Filter bar')}>
              <div className="switch-label">Show map</div>
              <div className="switch u-mobile-display-none">
                <input
                  id="switch-primary"
                  onChange={this.toggleSwitch.bind(this)}
                  name="switch-primary"
                  type="checkbox" />
                <label htmlFor="switch-primary" className="primary-color" />
              </div>
              <div className="btn-group u-desktop-display-none">
                <button className="btn btn--light" onClick={this.hideMap.bind(this)}><i className="fa fa-list" /></button>
                <button className="btn btn--light" onClick={this.hideList.bind(this)}><i className="fa fa-map" /></button>
              </div>
            </div>
          </div>
        </div>
        { this.state.showListMap
          ? <div className="map-list-combined">
            <div id="list" className="list-container map-list-combined__list">
              <PlansList key="content" items={this.state.items} />
            </div>
            <div id="map" className="map-container map-list-combined__map u-mobile-display-none">
              <StickyBox offsetTop={0} offsetBottom={0}>
                <PlansMap key="content"
                  resize={this.state.resizeMap}
                  items={this.state.items}
                  bounds={this.props.bounds}
                  districts={this.props.districts}
                  baseurl={this.props.baseurl}
                  districtnames={this.props.districtnames} />
              </StickyBox>
            </div>
          </div>
          : <div className="map-list-combined">
            <div className="list-container map-list-combined__list">
              <PlansList key="content" items={this.state.items} />
            </div>
          </div>
        }
      </div>
    )
  }
}

module.exports = ListMapBox
