/* global django */
const React = require('react')
const L = require('leaflet')
const $ = require('jquery')
require('mapbox-gl-leaflet')

const addressIcon = L.icon({
  iconUrl: '/static/images/address_search_marker.svg',
  shadowUrl: '/static/images/map_shadow_01.svg',
  iconSize: [30, 36],
  iconAnchor: [15, 36],
  shadowSize: [40, 54],
  shadowAnchor: [20, 54],
  zIndexOffset: 1000
})

const pointToLatLng = function (point) {
  if (point.geometry !== '') {
    return {
      lat: point.geometry.coordinates[1],
      lng: point.geometry.coordinates[0]
    }
  }
}

const apiUrl = 'https://bplan-prod.liqd.net/api/addresses/'

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
      showInfoBox: true,
      showInfoBoxUser: true,
      filters: {
        status: -1,
        participation: -1,
        district: -1
      }
    }
  }

  componentWillReceiveProps (nextProps) {
    if (nextProps.resize === true) {
      this.map.eachLayer(function (layer) {
        this.map.removeLayer(layer)
      }.bind(this))
    }
  }

  componentDidMount () {
    this.map = this.createMap()
    this.addBackgroundMap(this.map)
    this.addDistrictLayers(this.map)
    this.cluster = L.markerClusterGroup({
      showCoverageOnHover: false
    }).addTo(this.map)
    this.markers = this.addMarkers(this.cluster)
  }

  componentDidUpdate () {
    if (this.props.resize === true) {
      this.map.invalidateSize()
      this.addBackgroundMap(this.map)
      this.addDistrictLayers(this.map)
      this.cluster = L.markerClusterGroup({
        showCoverageOnHover: false
      }).addTo(this.map)
      this.markers = this.addMarkers(this.cluster)
    } else {
      this.cluster.clearLayers()
      this.markers = this.addMarkers(this.cluster)
    }
  }

  escapeHtml (unsafe) {
    return $('<div>').text(unsafe).html()
  }

  bindMap (element) {
    this.mapElement = element
  }

  createMap () {
    var map = new L.Map(this.mapElement, {
      scrollWheelZoom: false,
      zoomControl: false,
      maxZoom: 18 })
    new L.Control.Zoom({ position: 'bottomright' }).addTo(map)
    return map
  }

  addBackgroundMap (map) {
    L.mapboxGL({
      accessToken: 'no-token',
      style: this.props.baseurl
    }).addTo(map)
    map.fitBounds(this.props.bounds)
    map.options.minZoom = map.getZoom()
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

  displayResults (geojson) {
    this.setState(
      { 'displayResults': true,
        'showInfoBox': false,
        'searchResults': geojson.features }
    )
  }

  displayErrorMessage () {
    this.setState(
      { 'displayError': true,
        'showInfoBox': false }
    )
    setTimeout(function () {
      this.setState(
        { 'displayError': false,
          'showInfoBox': this.state.showInfoBoxUser })
    }.bind(this), 2000)
  }

  displayAdressMarker (geojson) {
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
      { 'address': addressMarker,
        'showInfoBox': this.state.showInfoBoxUser }
    )
  }

  onAddressSearchSubmit (event) {
    event.preventDefault()
    let address = event.target.search.value
    $.ajax(apiUrl, {
      data: { address: address },
      context: this,
      success: function (geojson) {
        let count = geojson.count
        if (count === 0) {
          this.displayErrorMessage()
        } else if (count === 1) {
          this.displayAdressMarker(geojson)
        } else {
          this.displayResults(geojson)
        }
      }
    })
  }

  onAddressSearchChange (event) {
    if (event.target.value === '' && this.state.address) {
      this.map.removeLayer(this.state.address)
      this.setState({
        'address': null
      })
    }
  }

  selectSearchResult (event) {
    let index = parseInt(event.target.value, 10)
    let address = this.state.searchResults[index]
    this.displayAdressMarker(address)
    this.setState(
      { 'displayResults': false }
    )
  }

  closeInfoBox () {
    this.setState(
      { 'showInfoBox': false,
        'showInfoBoxUser': false }
    )
  }

  render () {
    return (
      <div className="map-list-combined__map" ref={this.bindMap.bind(this)}>
        <div className="map-list-combined__map__search">
          <form onSubmit={this.onAddressSearchSubmit.bind(this)} data-embed-target="ignore" className="input-group form-group">
            <input
              onChange={this.onAddressSearchChange.bind(this)}
              className="input-group__input"
              name="search"
              type="search"
              placeholder={django.gettext('Address Search')} />
            <button className="input-group__after btn btn--light" type="submit" title={django.gettext('Search')}>
              <i className="fas fa-location-arrow" aria-label={django.gettext('Search')} />
            </button>

            {this.state.displayResults &&
              <ul aria-labelledby="id_filter_address">
                { this.state.searchResults.map((name, i) => {
                  return (
                    <li key={i}>
                      <button
                        type="button"
                        value={i}
                        onClick={this.selectSearchResult.bind(this)}>
                        {name.properties.strname} {name.properties.hsnr} in {name.properties.plz} {name.properties.bezirk_name}
                      </button>
                    </li>
                  )
                })
                }
              </ul>
            }

            {this.state.displayError &&
              <ul aria-labelledby="id_filter_address" className="map-list-combined__map__search__error">
                <li>{django.gettext('Nothing to show')}</li>
              </ul>
            }

          </form>
        </div>
        {this.state.showInfoBox &&
        <div className="map-infobox">
          <button className="infobox__close" id="close" aria-label={django.gettext('Close information box')} onClick={this.closeInfoBox.bind(this)}><i className="fa fa-times" /></button>
          <i className="fa fa-info-circle" aria-hidden="true" /><span>{django.gettext('Projects without spacial reference are not shown on the map. Please have a look at the project list.')}</span>
        </div>
        }
      </div>
    )
  }
}

module.exports = PlansMap
