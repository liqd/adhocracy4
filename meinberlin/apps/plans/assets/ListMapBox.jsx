/* global history */
import StickyBox from 'react-sticky-box'
const React = require('react')
let PlansList = require('./PlansList')
let PlansMap = require('./PlansMap')
let FilterNav = require('./FilterNav')
let ListMapSwitch = require('./MapListSwitch')

const breakpointXS = 800
const breakpointMD = 1024

class ListMapBox extends React.Component {
  constructor (props) {
    super(props)

    this.windowSizeChange = this.handleWindowSizeChange.bind(this)
    this.location = window.location.pathname

    this.state = {
      width: window.innerWidth,
      items: [],
      searchResults: null,
      address: null,
      selected: null,
      displayError: false,
      displayResults: false,
      showListMap: window.innerWidth > breakpointMD,
      resizeMap: false,
      filterChanged: false,
      status: -1,
      participation: -1,
      district: props.selectedDistrict,
      topic: props.selectedTopic
    }
  }

  handleWindowSizeChange () {
    let width = window.innerWidth
    this.setState({
      width: width
    })
  }

  componentWillMount () {
    window.addEventListener('resize', this.windowSizeChange)
  }

  componentWillUnmount () {
    window.removeEventListener('resize', this.windowSizeChange)
  }

  componentDidMount () {
    this.updateList()
  }

  componentDidUpdate () {
    if (this.state.filterChanged === true) {
      this.updateList()
    }
  }

  isInFilter (item) {
    return (this.state.topic === '-1' || item.topics.includes(this.state.topic)) &&
      (this.state.district === '-1' || this.state.district === item.district)
  }

  updateList () {
    let items = []
    this.props.initialitems.forEach((item, i) => {
      if (this.isInFilter(item)) {
        items.push(item)
      }
    })
    let showListMap = this.state.showListMap
    if (window.innerWidth <= breakpointMD) {
      showListMap = false
    }
    this.setState({
      items: items,
      filterChanged: false,
      showListMap: showListMap
    })
  }

  toggleSwitch () {
    let newValue = !this.state.showListMap
    this.setState({ showListMap: newValue })
  }

  showList () {
    this.setState({ showListMap: false })
  }

  showMap () {
    this.setState({ showListMap: true })
  }

  updateUrl (topic, district) {
    let params = '?district=' + district + '&topic=' + topic
    let newUrl = this.location + params
    if (window.history && history.pushState) {
      window.history.replaceState({}, '', newUrl)
    }
  }

  selectDistrict (district) {
    var newDistrict = (district === '-1') ? '-1' : this.props.districtnames[district]
    this.setState({
      filterChanged: true,
      district: newDistrict
    })
    this.updateUrl(this.state.topic, newDistrict)
  }

  selectTopic (topic) {
    this.setState({
      filterChanged: true,
      topic: topic
    })
    this.updateUrl(topic, this.state.district)
  }

  getPlansList (isHorizontal) {
    return (
      <PlansList
        key="content"
        items={this.state.items}
        topicChoices={this.props.topicChoices}
        isHorizontal={isHorizontal}
      />
    )
  }

  getPlansMap () {
    return (
      <PlansMap key="content"
        resize={this.state.resizeMap}
        items={this.state.items}
        bounds={this.props.bounds}
        currentDistrict={this.state.district}
        nonValue={this.props.districtnames[this.props.districtnames.length - 1]}
        districts={this.props.districts}
        baseurl={this.props.baseurl}
        districtnames={this.props.districtnames}
        topicChoices={this.props.topicChoices}
      />
    )
  }

  render () {
    const { width } = this.state
    const isMobile = width <= breakpointXS
    const isTablet = width <= breakpointMD && width > breakpointXS

    if (isMobile) {
      return (
        <div>
          <FilterNav
            selectDistrict={this.selectDistrict.bind(this)}
            selectTopic={this.selectTopic.bind(this)}
            district={this.state.district}
            districtnames={this.props.districtnames}
            topic={this.state.topic}
            topicChoices={this.props.topicChoices}
            numColumns={1}
            isStacked
          />
          <ListMapSwitch
            toggleSwitch={this.toggleSwitch.bind(this)}
            showMap={this.showMap.bind(this)}
            showList={this.showList.bind(this)}
            isSlider={false}
            displayMap={this.state.showListMap}
          />
          {!this.state.showListMap &&
            this.getPlansList(false)
          }
          {this.state.showListMap &&
            this.getPlansMap()
          }
        </div>)
    } else if (isTablet) {
      return (<div>
        <FilterNav
          selectDistrict={this.selectDistrict.bind(this)}
          selectTopic={this.selectTopic.bind(this)}
          district={this.state.district}
          districtnames={this.props.districtnames}
          topic={this.state.topic}
          topicChoices={this.props.topicChoices}
          numColumns={2}
          isStacked={false}
        />
        <ListMapSwitch
          toggleSwitch={this.toggleSwitch.bind(this)}
          showMap={this.showMap.bind(this)}
          showList={this.showList.bind(this)}
          isSlider={false}
          displayMap={this.state.showListMap}
        />
        {!this.state.showListMap &&
          this.getPlansList(false)
        }
        {this.state.showListMap &&
          this.getPlansMap()
        }
      </div>)
    } else {
      return (
        <div>
          <FilterNav
            selectDistrict={this.selectDistrict.bind(this)}
            selectTopic={this.selectTopic.bind(this)}
            district={this.state.district}
            districtnames={this.props.districtnames}
            topic={this.state.topic}
            topicChoices={this.props.topicChoices}
            numColumns={3}
            isStacked={false}
          />
          <ListMapSwitch
            toggleSwitch={this.toggleSwitch.bind(this)}
            showMap={this.showMap.bind(this)}
            showList={this.showList.bind(this)}
            isSlider
            displayMap={this.state.showListMap}

          />
          { this.state.showListMap
            ? <div className="map-list-combined">
              <div id="list" className="list-container map-list-combined__list">
                { this.getPlansList(true) }
              </div>
              <div id="map" className="map-container map-list-combined__map">
                <StickyBox offsetTop={0} offsetBottom={0}>
                  { this.getPlansMap() }
                </StickyBox>
              </div>
            </div>
            : <div className="l-wrapper">
              <div className="map-list-combined">
                <div className="list-container map-list-combined__list">
                  { this.getPlansList(false) }
                </div>
              </div>
            </div>
          }
        </div>)
    }
  }
}

module.exports = ListMapBox
