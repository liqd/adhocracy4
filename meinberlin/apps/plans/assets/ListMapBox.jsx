/* global history */
/* global django */
import StickyBox from 'react-sticky-box'
const React = require('react')
let PlansList = require('./PlansList')
let PlansMap = require('./PlansMap')
let FilterNav = require('./FilterNav')
let Toggles = require('./Toggles')

const breakpointXS = 512
const breakpointMD = 1024

const participationNames = [
  django.gettext('with participation'),
  django.gettext('without participation'),
  django.gettext('undecided')
]

const statusNames = [
  django.gettext('ongoing'),
  django.gettext('done')
]

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
      status: 0,
      participation: 0,
      district: props.selectedDistrict,
      topic: props.selectedTopic,
      organisation: '-1',
      titleSearch: '-1'
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
      (this.state.district === '-1' || this.state.district === item.district) &&
      (this.state.participation === -1 || this.state.participation === item.participation) &&
      (this.state.status === -1 || this.state.status === item.status) &&
      (this.state.organisation === '-1' || this.state.organisation === item.organisation)
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

  selectParticipation (participation) {
    this.setState({
      filterChanged: true,
      participation: participation
    })
  }

  selectStatus (status) {
    this.setState({
      filterChanged: true,
      status: status
    })
  }

  selectOrganisation (organisation) {
    var newOrganisation = (organisation === '-1') ? '-1' : this.props.organisations[organisation]
    this.setState({
      filterChanged: true,
      organisation: newOrganisation
    })
  }

  selectTitleSearch (searchTerm) {
    this.setState({
      filterChanged: true,
      titleSearch: searchTerm
    })
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
            selectParticipation={this.selectParticipation.bind(this)}
            selectStatus={this.selectStatus.bind(this)}
            selectOrganisation={this.selectOrganisation.bind(this)}
            selectTitleSearch={this.selectTitleSearch.bind(this)}
            district={this.state.district}
            districtnames={this.props.districtnames}
            topic={this.state.topic}
            topicChoices={this.props.topicChoices}
            participation={this.state.participation}
            participationNames={participationNames}
            status={this.state.status}
            statusNames={statusNames}
            organisation={this.state.organisation}
            organisations={this.props.organisations}
            titleSearch={this.state.titleSearch}
            numColumns={1}
            isStacked
            isTablet={isTablet}
          />
          <Toggles
            toggleSwitch={this.toggleSwitch.bind(this)}
            showMap={this.showMap.bind(this)}
            showList={this.showList.bind(this)}
            statusString={statusNames[this.state.status]}
            statusSelected={this.state.status !== -1}
            changeStatusSelection={this.selectStatus.bind(this)}
            participationString={participationNames[this.state.participation]}
            participationSelected={this.state.participation !== -1}
            changeParticipationSelection={this.selectParticipation.bind(this)}
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
          selectParticipation={this.selectParticipation.bind(this)}
          selectStatus={this.selectStatus.bind(this)}
          selectOrganisation={this.selectOrganisation.bind(this)}
          selectTitleSearch={this.selectTitleSearch.bind(this)}
          district={this.state.district}
          districtnames={this.props.districtnames}
          topic={this.state.topic}
          topicChoices={this.props.topicChoices}
          participation={this.state.participation}
          participationNames={participationNames}
          status={this.state.status}
          statusNames={statusNames}
          organisation={this.state.organisation}
          organisations={this.props.organisations}
          titleSearch={this.state.titleSearch}
          numColumns={2}
          isStacked={false}
          isTablet={isTablet}
        />
        <Toggles
          toggleSwitch={this.toggleSwitch.bind(this)}
          showMap={this.showMap.bind(this)}
          showList={this.showList.bind(this)}
          statusString={statusNames[this.state.status]}
          statusSelected={this.state.status !== -1}
          changeStatusSelection={this.selectStatus.bind(this)}
          participationString={participationNames[this.state.participation]}
          participationSelected={this.state.participation !== -1}
          changeParticipationSelection={this.selectParticipation.bind(this)}
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
            selectParticipation={this.selectParticipation.bind(this)}
            selectStatus={this.selectStatus.bind(this)}
            selectOrganisation={this.selectOrganisation.bind(this)}
            selectTitleSearch={this.selectTitleSearch.bind(this)}
            district={this.state.district}
            districtnames={this.props.districtnames}
            topic={this.state.topic}
            topicChoices={this.props.topicChoices}
            participation={this.state.participation}
            participationNames={participationNames}
            status={this.state.status}
            statusNames={statusNames}
            organisation={this.state.organisation}
            organisations={this.props.organisations}
            titleSearch={this.state.titleSearch}
            numColumns={3}
            isStacked={false}
            isTablet={isTablet}
          />
          <Toggles
            toggleSwitch={this.toggleSwitch.bind(this)}
            showMap={this.showMap.bind(this)}
            showList={this.showList.bind(this)}
            statusString={statusNames[this.state.status]}
            statusSelected={this.state.status !== -1}
            changeStatusSelection={this.selectStatus.bind(this)}
            participationString={participationNames[this.state.participation]}
            participationSelected={this.state.participation !== -1}
            changeParticipationSelection={this.selectParticipation.bind(this)}
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
