/* global django */

const apiUrl = 'https://bplan-prod.liqd.net/api/addresses/'
const React = require('react')
const ReactDOM = require('react-dom')
const update = require('immutability-helper')
const $ = require('jquery')
const L = require('leaflet')

const statusNames = [
  django.gettext('Idea'),
  django.gettext('Planning'),
  django.gettext('Implementation'),
  django.gettext('Done'),
  django.gettext('Stopped')
]

const statusIconNames = [
  'lightbulb-o',
  'cogs',
  'play',
  'check',
  'pause'
]

const participationNames = [
  django.gettext('No'),
  django.gettext('Yes'),
  django.gettext('Still undecided')
]

const icons = statusIconNames.map((cls, i) => L.divIcon({
  className: 'map-list-combined__icon',
  html: `<i class="fa fa-${cls}" title="${statusNames[i]}" aria-hidden="true"></i>`,
  iconSize: [20, 20]
}))

const activeIcon = L.icon({
  iconUrl: '/static/images/map_pin_01_2x.png',
  shadowUrl: '/static/images/map_shadow_01_2x.png',
  iconSize: [30, 45],
  iconAnchor: [15, 45],
  shadowSize: [40, 54],
  shadowAnchor: [20, 54],
  zIndexOffset: 1000
})

const addressIcon = L.icon({
  iconUrl: '/static/images/address_search_marker.png',
  shadowUrl: '/static/images/map_shadow_01_2x.png',
  iconSize: [30, 45],
  iconAnchor: [15, 45],
  shadowSize: [40, 54],
  shadowAnchor: [20, 54],
  zIndexOffset: 1000
})

const districtStyle = {
  'color': '#253276',
  'weight': 1,
  'opacity': 1,
  'fillOpacity': 0
}

const pointToLatLng = function (point) {
  return {
    lat: point.geometry.coordinates[1],
    lng: point.geometry.coordinates[0]
  }
}

const checkQueryMatch = function (item, q) {
  const s = [
    item.title,
    item.organisation,
    item.category
  ].join(' ').toLowerCase()
  return !q || q.split(/\s+/g).every(word => {
    return s.indexOf(word.toLowerCase()) !== -1
  })
}

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

  bindList (element) {
    this.listElement = element
  }

  bindMap (element) {
    this.mapElement = element
  }

  onBoundsChange (event) {
    this.setState({
      filters: update(this.state.filters, {
        $merge: {bounds: event.target.getBounds()}
      })
    })
  }

  onStatusFilterChange (event) {
    this.setState({
      filters: update(this.state.filters, {
        $merge: {status: parseInt(event.currentTarget.value, 10)}
      })
    })
  }

  onParticipationFilterChange (event) {
    this.setState({
      filters: update(this.state.filters, {
        $merge: {participation: parseInt(event.currentTarget.value, 10)}
      })
    })
  }

  onFreeTextFilterChange (event) {
    this.setState({
      filters: update(this.state.filters, {
        $merge: {q: event.target.value}
      })
    })
  }

  onFreeTextFilterSubmit (event) {
    event.preventDefault()
    this.onFreeTextFilterChange({
      target: event.target.search
    })
  }

  onDistrictFilterChange (event) {
    this.setState({
      filters: update(this.state.filters, {
        $merge: {district: parseInt(event.currentTarget.value, 10)}
      })
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

  onAddressSearchSubmit (event) {
    event.preventDefault()
    let address = event.target.search.value
    $.ajax(apiUrl, {
      data: {address: address},
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

  displayResults (geojson) {
    this.setState(
      {'displayResults': true,
        'searchResults': geojson.features}
    )
  }

  selectSearchResult (event) {
    let index = parseInt(event.target.value, 10)
    let address = this.state.searchResults[index]
    this.displayAdressMarker(address)
    this.setState(
      {'displayResults': false}
    )
  }

  displayAdressMarker (geojson) {
    if (this.state.address) {
      this.map.removeLayer(this.state.address)
    }
    let addressMarker = L.geoJSON(geojson, {
      pointToLayer: function (feature, latlng) {
        return L.marker(latlng, {icon: addressIcon})
      }
    }).addTo(this.map)
    this.map.flyToBounds(addressMarker.getBounds(), {'maxZoom': 13})
    this.setState(
      {'address': addressMarker}
    )
  }

  displayErrorMessage () {
    this.setState(
      {'displayError': true}
    )
    setTimeout(function () {
      this.setState(
        {'displayError': false})
    }.bind(this), 2000)
  }

  onSelect (i) {
    this.setState({
      selected: i
    })
  }

  createMap () {
    var basemap = this.props.baseurl + '{z}/{x}/{y}.png'
    var baselayer = L.tileLayer(basemap, {
      attribution: this.props.attribution
    })
    var map = new L.Map(this.mapElement, { scrollWheelZoom: false })
    baselayer.addTo(map)

    map.fitBounds(this.props.bounds)
    map.options.minZoom = map.getZoom()

    return map
  }

  isInFilter (item) {
    let filters = this.state.filters
    return (filters.status === -1 || filters.status === item.status) &&
      (filters.district === -1 || this.props.districtnames[filters.district] === item.district) &&
      (filters.participation === -1 || filters.participation === item.participation) &&
      checkQueryMatch(item, filters.q) &&
      (!filters.bounds || filters.bounds.contains(pointToLatLng(item.point)))
  }

  setMarkerSelected (i, item) {
    let activeMarker = this.activeMarkers[i]
    let marker = this.markers[i]

    if (!this.selected.hasLayer(activeMarker)) {
      this.cluster.removeLayer(marker)
      this.selected.clearLayers()

      // Removing a marker from a layer resets its zIndexOffset,
      // thus the zIndexOffset of the selected marker has to be set
      // after it is removed from the cluster to rise it to the front.
      marker.setZIndexOffset(1000)
      activeMarker.setZIndexOffset(1001)
      this.selected.addLayer(marker)
      this.selected.addLayer(activeMarker)
    }
  }

  setMarkerDefault (i, item) {
    let marker = this.markers[i]
    if (!this.cluster.hasLayer(marker)) {
      this.selected.removeLayer(marker)
      this.selected.removeLayer(this.activeMarkers[i])

      marker.setZIndexOffset(0)
      this.cluster.addLayer(marker)
    }
  }

  setMarkerFiltered (i) {
    // Remove the items markers from every possible layer.
    this.cluster.removeLayer(this.markers[i])
    this.selected.removeLayer(this.markers[i])
    this.selected.removeLayer(this.activeMarkers[i])
  }

  componentDidMount () {
    this.map = this.createMap()
    this.cluster = L.markerClusterGroup({
      showCoverageOnHover: false
    }).addTo(this.map)
    this.selected = L.layerGroup().addTo(this.map)

    L.geoJSON(this.props.districts, {style: districtStyle}).addTo(this.map)

    this.markers = this.props.items.map((item, i) => {
      let marker = L.marker(pointToLatLng(item.point), {icon: icons[item.status]})
      this.cluster.addLayer(marker)
      marker.on('click', () => {
        this.onSelect(i)
      })
      return marker
    })

    this.activeMarkers = this.props.items.map((item, i) => {
      let marker = L.marker(pointToLatLng(item.point), {icon: activeIcon})
      marker.on('click', () => {
        this.onSelect(i)
      })
      return marker
    })

    this.map.on('zoomend', this.onBoundsChange.bind(this))
    this.map.on('moveend', this.onBoundsChange.bind(this))
  }

  componentDidUpdate (prevProps, prevState) {
    if (prevState.selected !== this.state.selected || prevState.filters !== this.state.filters) {
      // filter markers
      this.props.items.forEach((item, i) => {
        if (!this.isInFilter(item)) {
          this.setMarkerFiltered(i)
        } else if (i === this.state.selected) {
          this.setMarkerSelected(i, item)
        } else {
          this.setMarkerDefault(i, item)
        }
      })

      // scroll list
      if (this.state.selected !== null && this.isInFilter(this.props.items[this.state.selected])) {
        $(this.listElement).find('.selected').scrollintoview()
      } else {
        this.listElement.scrollTo(0, 0)
      }
    }
  }

  renderListItem (item, i) {
    let className = 'list-item list-item--squashed'
    if (i === this.state.selected) {
      className += ' selected'
    }

    return (
      <li className={className} key={i} onFocus={(e) => { this.onSelect(i) }} tabIndex="0">
        <div className="list-item__subtitle">{item.organisation}</div>
        <h3 className="list-item__title"><a href={item.url}>{item.title}</a></h3>
        <div className="list-item__labels">
          {
            <span className="label label--secondary">{item.status_display}</span>
          } {item.category &&
            <span className="label">{item.category}</span>
          } {item.point_label &&
            <span className="label"><i className="fa fa-map-marker" aria-hidden="true" /> {item.point_label}</span>
          }
        </div>
      </li>
    )
  }

  renderList () {
    let list = []
    this.props.items.forEach((item, i) => {
      if (this.isInFilter(item)) {
        list.push(this.renderListItem(item, i))
      }
    })

    if (list.length > 0) {
      return (
        <ul className="u-list-reset">
          {list}
        </ul>
      )
    } else {
      return (
        <div className="list-item-empty">{django.gettext('Nothing to show')}</div>
      )
    }
  }

  render () {
    return (
      <div>
        <div className="l-wrapper">
          <div className="control-bar" role="group" aria-label={django.gettext('Filter bar')}>
            <form onSubmit={this.onAddressSearchSubmit.bind(this)} data-embed-target="ignore" className="input-group form-group u-inline-flex u-position-relative">
              <input
                onChange={this.onAddressSearchChange.bind(this)}
                className="input-group__input"
                name="search"
                type="search"
                placeholder={django.gettext('Address Search')} />
              <button className="input-group__after btn btn--light" type="submit" title={django.gettext('Search')}>
                <i className="fa fa-search" aria-label={django.gettext('Search')} />
              </button>
              {this.state.displayResults &&
              <ul aria-labelledby="id_filter_address" className="map-list-combined__dropdown-menu">
                { this.state.searchResults.map((name, i) => {
                  return (
                    <li key={i}>
                      <button
                        type="button"
                        className="dropdown-item"
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
            </form>
            &nbsp;
            <form onSubmit={this.onFreeTextFilterSubmit.bind(this)} data-embed-target="ignore" className="input-group form-group u-inline-flex">
              <input
                onChange={this.onFreeTextFilterChange.bind(this)}
                className="input-group__input"
                name="search"
                type="search"
                placeholder={django.gettext('Search')} />
              <button className="input-group__after btn btn--light" type="submit" title={django.gettext('Search')}>
                <i className="fa fa-search" aria-label={django.gettext('Search')} />
              </button>
            </form>
            &nbsp;
            <div className="dropdown ">
              <button type="button" className="dropdown-toggle btn btn--light btn--select" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" id="id_filter_status">
                {django.gettext('Status')}: {statusNames[this.state.filters.status] || django.gettext('All')}
                <i className="fa fa-caret-down" aria-hidden="true" />
              </button>
              <ul aria-labelledby="id_filter_status" className="dropdown-menu">
                <li>
                  <button
                    type="button"
                    className="dropdown-item select-item"
                    value="-1"
                    onClick={this.onStatusFilterChange.bind(this)}>
                    {django.gettext('All')}
                  </button>
                </li>
                {
                  statusNames.map((name, i) => {
                    return (
                      <li key={i}>
                        <button
                          type="button"
                          className="dropdown-item select-item"
                          value={i}
                          onClick={this.onStatusFilterChange.bind(this)}>
                          <i className={`select-item-indicator fa fa-${statusIconNames[i]}`} aria-hidden="true" />
                          {name}
                        </button>
                      </li>
                    )
                  })
                }
              </ul>
            </div>
            &nbsp;
            <div className="dropdown ">
              <button type="button" className="dropdown-toggle btn btn--light btn--select" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" id="id_filter_participation">
                {django.gettext('Participation')}: {participationNames[this.state.filters.participation] || django.gettext('All')}
                <i className="fa fa-caret-down" aria-hidden="true" />
              </button>
              <ul aria-labelledby="id_filter_participation" className="dropdown-menu">
                <li>
                  <button
                    type="button"
                    className="dropdown-item"
                    value="-1"
                    onClick={this.onParticipationFilterChange.bind(this)}>
                    {django.gettext('All')}
                  </button>
                </li>
                {
                  participationNames.map((name, i) => {
                    return (
                      <li key={i}>
                        <button
                          type="button"
                          className="dropdown-item"
                          value={i}
                          onClick={this.onParticipationFilterChange.bind(this)}>
                          {name}
                        </button>
                      </li>
                    )
                  })
                }
              </ul>
            </div>
            &nbsp;
            <div className="dropdown ">
              <button type="button" className="dropdown-toggle btn btn--light btn--select" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" id="id_filter_district">
                {django.gettext('District')}: {this.props.districtnames[this.state.filters.district] || django.gettext('All')}
                <i className="fa fa-caret-down" aria-hidden="true" />
              </button>
              <ul aria-labelledby="id_filter_district" className="dropdown-menu">
                <li>
                  <button
                    type="button"
                    className="dropdown-item"
                    value="-1"
                    onClick={this.onDistrictFilterChange.bind(this)}>
                    {django.gettext('All')}
                  </button>
                </li>
                {
                  this.props.districtnames.map((name, i) => {
                    return (
                      <li key={i}>
                        <button
                          type="button"
                          className="dropdown-item"
                          value={i}
                          onClick={this.onDistrictFilterChange.bind(this)}>
                          {name}
                        </button>
                      </li>
                    )
                  })
                }
              </ul>
            </div>
          </div>
        </div>

        <div className="map-list-combined">
          {this.state.displayError &&
            <div className="alert alert-error map-list-combined__alert">{django.gettext('Address could not be found')}</div>
          }
          <div className="map-list-combined__map" ref={this.bindMap.bind(this)} />
          <div className="map-list-combined__list" ref={this.bindList.bind(this)}>
            {this.renderList()}
          </div>
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
    ReactDOM.render(<PlansMap items={items} attribution={attribution} baseurl={baseurl} bounds={bounds} districts={districts} districtnames={districtnames} />, element)
  })
}

$(init)
$(document).on('a4.embed.ready', init)
