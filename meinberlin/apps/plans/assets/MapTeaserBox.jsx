const React = require('react')
const FilterNav = require('./FilterNav')

const breakpointXS = 800
const breakpointMD = 1024

class MapTeaserBox extends React.Component {
  constructor (props) {
    super(props)
    this.windowSizeChange = this.handleWindowSizeChange.bind(this)

    this.state = {
      width: window.innerWidth,
      filterChanged: false,
      linkUrl: this.props.url,
      district: '-1',
      topic: '-1'
    }
  }

  handleWindowSizeChange () {
    const width = window.innerWidth
    this.setState({
      width
    })
  }

  UNSAFE_componentWillMount () {
    window.addEventListener('resize', this.windowSizeChange)
  }

  componentWillUnmount () {
    window.removeEventListener('resize', this.windowSizeChange)
  }

  selectDistrict (district) {
    let districtName = this.props.districtnames[district]
    if (district === '-1') {
      districtName = '-1'
    }
    const newLinkUrl = this.props.url + '?district=' + districtName + '&topic=' + this.state.topic
    this.setState({
      district: districtName,
      linkUrl: newLinkUrl
    })
  }

  selectTopic (topic) {
    const newLinkUrl = this.props.url + '?district=' + this.state.district + '&topic=' + topic
    this.setState({
      topic,
      linkUrl: newLinkUrl
    })
  }

  render () {
    const { width } = this.state
    const isMobile = width <= breakpointXS
    const isTablet = width <= breakpointMD && width > breakpointXS

    if (isMobile) {
      return (
        <FilterNav
          selectDistrict={this.selectDistrict.bind(this)}
          selectTopic={this.selectTopic.bind(this)}
          district={this.state.district}
          districtnames={this.props.districtnames}
          topic={this.state.topic}
          topicChoices={this.props.topicChoices}
          numColumns={1}
          linkUrl={this.state.linkUrl}
          isStacked
        />
      )
    } else if (isTablet) {
      return (
        <FilterNav
          selectDistrict={this.selectDistrict.bind(this)}
          selectTopic={this.selectTopic.bind(this)}
          district={this.state.district}
          districtnames={this.props.districtnames}
          topic={this.state.topic}
          topicChoices={this.props.topicChoices}
          numColumns={2}
          linkUrl={this.state.linkUrl}
          isStacked={false}
        />
      )
    } else {
      return (
        <FilterNav
          selectDistrict={this.selectDistrict.bind(this)}
          selectTopic={this.selectTopic.bind(this)}
          district={this.state.district}
          districtnames={this.props.districtnames}
          topic={this.state.topic}
          topicChoices={this.props.topicChoices}
          numColumns={3}
          linkUrl={this.state.linkUrl}
          isStacked={false}
        />
      )
    }
  }
}

module.exports = MapTeaserBox
