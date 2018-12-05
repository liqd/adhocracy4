/* global $ */
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
const pointToLatLng = function (point) {
  if (point.geometry !== '') {
    return {
      lat: point.geometry.coordinates[1],
      lng: point.geometry.coordinates[0]
    }
  }
}

const statusIconNames = [
  'idee',
  'planung',
  'implementiert',
  'beendet',
  'pause'
]

const statusIconPins = statusIconNames.map((cls, i) => L.icon({
  iconUrl: `/static/plan_icons/pins/${cls}_pin.svg`,
  shadowUrl: '/static/images/map_shadow_01.svg',
  iconSize: [30, 36],
  iconAnchor: [15, 36],
  shadowSize: [40, 54],
  shadowAnchor: [20, 54],
  zIndexOffset: 1000
}))

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

  escapeHtml (unsafe) {
    return $('<div>').text(unsafe).html()
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

  addDistrictLayers (map) {
    let districtStyle = {
      'color': '#253276',
      'weight': 1,
      'opacity': 1,
      'fillOpacity': 0
    }
    L.geoJSON(this.props.districts, { style: districtStyle }).addTo(map)
  }

  getPopUpContent (item) {
    let popupContent = '<div class="maps-popups-popup-text-content">' +
                             '<div class="maps-popups-popup-name">' +
                                '<a href="' + item.url + '">' + this.escapeHtml(item.title) + '</a>' +
                            '</div>' +
                          '</div>'
    return popupContent
  }

  addMarkers (cluster) {
    this.props.items.map((item, i) => {
      if (item.point !== '') {
        let marker = L.marker(pointToLatLng(item.point), { icon: statusIconPins[item.status] })
        cluster.addLayer(marker)
        marker.bindPopup(this.getPopUpContent(item))
        return marker
      }
    })
  }

  componentDidMount () {
    this.map = this.createMap()
    this.addDistrictLayers(this.map)
    this.cluster = L.markerClusterGroup({
      showCoverageOnHover: false
    }).addTo(this.map)
    this.markers = this.addMarkers(this.cluster)
  }

  render () {
    return (
      <div className="map-list-combined__map" ref={this.bindMap.bind(this)} />
    )
  }
}

module.exports = PlansMap
