/* global django */

const React = require('react')
const ReactDOM = require('react-dom')
const $ = require('jquery')
const L = require('leaflet')
require('mapbox-gl-leaflet')



class PlansMap extends React.Component {
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

  bindMap (element) {
    this.mapElement = element
  }

  createMap () {
    var map = new L.Map(this.mapElement, { scrollWheelZoom: false, maxZoom: 18 })
    L.mapboxGL({
      accessToken: 'no-token',
      style: this.props.baseurl
    }).addTo(map)

    map.fitBounds(this.props.bounds)
    map.options.minZoom = map.getZoom()

    return map
  }

  componentDidMount () {
    this.map = this.createMap()
    this.cluster = L.markerClusterGroup({
      showCoverageOnHover: false
    }).addTo(this.map)
    this.selected = L.layerGroup().addTo(this.map)
  }

  render () {
    return (
      <div>

        <div className="map-list-combined">
          <div className="map-list-combined__list" >
          </div>
          <div className="map-list-combined__map" ref={this.bindMap.bind(this)} />
        </div>
      </div>
    )
  }
}

const init = function () {
  $('[data-map="plans"]').each(function (i, element) {
    let items = JSON.parse(element.getAttribute('data-items'))
    let attribution = element.getAttribute('data-attribution')
    let baseurl = element.getAttribute('data-baseurl')
    let bounds = JSON.parse(element.getAttribute('data-bounds'))
    let districts = JSON.parse(element.getAttribute('data-districts'))
    let districtnames = JSON.parse(element.getAttribute('data-district-names'))
    let exportUrl = element.getAttribute('data-export-url')
    ReactDOM.render(<PlansMap items={items} attribution={attribution} baseurl={baseurl} bounds={bounds} districts={districts} districtnames={districtnames} exportUrl={exportUrl} />, element)
  })
}

$(init)
$(document).on('a4.embed.ready', init)
