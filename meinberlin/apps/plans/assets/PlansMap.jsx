const React = require('react')
const L = require('leaflet')
require('mapbox-gl-leaflet')

/* const addressIcon = L.icon({
  iconUrl: '/static/images/address_search_marker.svg',
  shadowUrl: '/static/images/map_shadow_01.svg',
  iconSize: [30, 36],
  iconAnchor: [15, 36],
  shadowSize: [40, 54],
  shadowAnchor: [20, 54],
  zIndexOffset: 1000
}) */

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

  /* displayAdressMarker (geojson) {
    if (this.state.address) {
      this.map.removeLayer(this.state.address)
    }
    let addressMarker = L.geoJSON(geojson, {
      pointToLayer: function (feature, latlng) {
        return L.marker(latlng, { icon: addressIcon })
      }
    }).addTo(this.map)
    this.map.flyToBounds(addressMarker.getBounds(), { 'maxZoom': 13 })
    this.setState(
      { 'address': addressMarker }
    )
  } */

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
  }

  render () {
    return (
      <div className="map-list-combined__map" ref={this.bindMap.bind(this)} />
    )
  }
}

module.exports = PlansMap
