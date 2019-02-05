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
  django.gettext('with'),
  django.gettext('without'),
  django.gettext('undecided')
]

const participationButtonNames = [
  django.gettext('with participation'),
  django.gettext('without participation'),
  django.gettext('participation undecided')
]

const statusNames = [
  django.gettext('ongoing'),
  django.gettext('done')
]

class ListMapBox extends React.Component {
  constructor (props) {
    super(props)

    this.sortedItems = this.sortItems(this.props.initialitems)

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
      filterOpen: false,
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

  compareItems (item1, item2) {
    let item1Type = (item1.subtype === 'default' || item1.subtype === 'external') ? 'project' : item1.subtype
    let item2Type = (item2.subtype === 'default' || item2.subtype === 'external') ? 'project' : item2.subtype

    let sortByPhase = (phase1, phase2, earliestFirst) => {
      if (phase1 && phase2) {
        if (earliestFirst) {
          return (new Date(phase1) <= new Date(phase2)) ? -1 : 1
        } else {
          return (new Date(phase1) >= new Date(phase2)) ? -1 : 1
        }
      }
      if (phase1 || phase2) { return phase1 ? -1 : 1 }
      return false
    }

    if (item1Type === item2Type) {
      /* show
      1. projects with active phase
      2. projects with future phase
      3. projects with past phase
      4. projects without phase (can happen for external ones) */
      if (item1Type === 'project') {
        let active = sortByPhase(item1.active_phase[2], item2.active_phase[2], true)
        if (active) {
          return active
        }
        let future = sortByPhase(item1.future_phase, item2.future_phase, true)
        if (future) {
          return future
        }
        let past = sortByPhase(item1.past_phase, item2.past_phase, false)
        if (past) {
          return past
        }
      } else {
        /* sort plans and containers by modified */
        return (new Date(item1.created_or_modified) >= new Date(item2.created_or_modified)) ? -1 : 1
      }
    } else {
      /* show projects first, plans second, containers third */
      switch (item1Type) {
        case 'project':
          return -1
        case 'plan':
          return (item2Type === 'container') ? -1 : 1
        case 'container':
          return 1
      }
    }
  }

  sortItems (items) {
    let sortedItems = items.sort(this.compareItems)
    return sortedItems
  }

  isInTitle (title) {
    let titleLower = title.toLowerCase().trim().replace(/\s/g, '')
    let searchString = this.state.titleSearch.toLowerCase().trim()
    let searchList = searchString.split(/\s/)
    for (let i in searchList) {
      if (titleLower.indexOf(searchList[i]) === -1) {
        return false
      }
    }
    return true
  }

  isInFilter (item) {
    return (this.state.topic === '-1' || item.topics.includes(this.state.topic)) &&
      (this.state.district === '-1' || this.state.district === item.district) &&
      (this.state.participation === -1 || this.state.participation === item.participation) &&
      (this.state.status === -1 || this.state.status === item.status) &&
      (this.state.organisation === '-1' || this.state.organisation === item.organisation) &&
      (this.state.titleSearch === '-1' || this.isInTitle(item.title))
  }

  updateList () {
    let items = []
    this.sortedItems.forEach((item, i) => {
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

  toggleFilter (filterStatus) {
    this.setState({
      filterOpen: filterStatus
    })
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
    if (!Object.is(organisation, undefined)) {
      this.setState({
        filterChanged: true,
        organisation: organisation
      })
    } else {
      this.setState({
        filterChanged: true,
        organisation: '-1'
      })
    }
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

  getToggles (isSlider) {
    return (
      <Toggles
        toggleSwitch={this.toggleSwitch.bind(this)}
        showMap={this.showMap.bind(this)}
        showList={this.showList.bind(this)}
        titleSearchString={this.state.titleSearch}
        titleSearchSelected={this.state.titleSearch !== '-1'}
        changeTitleSearchSelection={this.selectTitleSearch.bind(this)}
        organisationString={this.state.organisation}
        organisationSelected={this.state.organisation !== '-1'}
        changeOrganisationSelection={this.selectOrganisation.bind(this)}
        statusString={statusNames[this.state.status]}
        statusSelected={this.state.status !== -1}
        changeStatusSelection={this.selectStatus.bind(this)}
        participationString={participationButtonNames[this.state.participation]}
        participationSelected={this.state.participation !== -1}
        changeParticipationSelection={this.selectParticipation.bind(this)}
        isSlider={isSlider}
        displayButtons={!this.state.filterOpen}
        displayMap={this.state.showListMap}
      />
    )
  }

  getFilterNav (numColumns, isStacked, isTablet) {
    return (
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
        numColumns={numColumns}
        updateFilterStatus={this.toggleFilter.bind(this)}
        isStacked={isStacked}
        isTablet={isTablet}
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
          {this.getFilterNav(1, true, isTablet)}
          {this.getToggles(false)}
          {!this.state.showListMap &&
            this.getPlansList(false)
          }
          {this.state.showListMap &&
            this.getPlansMap()
          }
        </div>)
    } else if (isTablet) {
      return (<div>
        {this.getFilterNav(2, false, isTablet)}
        {this.getToggles(false)}
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
          {this.getFilterNav(3, false, isTablet)}
          {this.getToggles(true)}
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
