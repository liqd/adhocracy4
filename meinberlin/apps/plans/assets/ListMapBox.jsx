import StickyBox from 'react-sticky-box'
const React = require('react')
let PlansList = require('./PlansList')
let PlansMap = require('./PlansMap')

class ListMapBox extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      searchResults: null,
      address: null,
      selected: null,
      displayError: false,
      displayResults: false,
      filters: {
        status: -1,
        participation: -1,
        district: -1
      }
    }
  }

  /* componentDidMount () {
   this.props.items.forEach((item, i) => {
   if (item.point !== '') {
   } if (i === this.state.selected) {
   this.setMarkerSelected(i, item)
   }
   })
   } */

  render () {
    return (
      <div className="map-list-combined">
        <div className="list-container map-list-combined__list">
          <PlansList key="content" items={this.props.items} />
        </div>
        <div className="map-container map-list-combined__map">
          <StickyBox offsetTop={0} offsetBottom={0}>
            <PlansMap key="content"
              items={this.props.items}
              bounds={this.props.bounds}
              districts={this.props.districts}
              baseurl={this.props.baseurl}
              districtnames={this.props.districtnames} />
          </StickyBox>
        </div>
      </div>
    )
  }
}

module.exports = ListMapBox
