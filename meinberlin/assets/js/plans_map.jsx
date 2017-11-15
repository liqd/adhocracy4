const React = require('react')
const ReactDOM = require('react-dom')
const update = require('immutability-helper')
const $ = require('jquery')
const L = require('leaflet')

const icon = L.icon({
  iconUrl: '/static/images/map_pin_01_2x.png',
  shadowUrl: '/static/images/map_shadow_01_2x.png',
  iconSize: [30, 45],
  iconAnchor: [15, 45],
  shadowSize: [40, 54],
  shadowAnchor: [20, 54]
})

const activeIcon = L.icon({
  iconUrl: '/static/images/map_pin_active_01_2x.png',
  shadowUrl: '/static/images/map_shadow_01_2x.png',
  iconSize: [30, 45],
  iconAnchor: [15, 45],
  shadowSize: [40, 54],
  shadowAnchor: [20, 54]
})

const pointToLatLng = function (point) {
  return {
    lat: point.geometry.coordinates[1],
    lng: point.geometry.coordinates[0]
  }
}

class PlansMap extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      selected: null,
      filters: {}
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
    return !filters.bounds || filters.bounds.contains(pointToLatLng(item.point))
  }

  componentDidMount () {
    this.map = this.createMap()
    this.cluster = L.markerClusterGroup({
      showCoverageOnHover: false
    }).addTo(this.map)
    this.selectedMarkers = L.layerGroup().addTo(this.map)

    this.markers = this.props.items.map((item, i) => {
      let marker = L.marker(pointToLatLng(item.point), {icon: icon})
      this.cluster.addLayer(marker)
      marker.on('click', () => {
        this.onSelect(i)
      })
      return marker
    })

    this.map.on('zoomend', this.onBoundsChange.bind(this))
    this.map.on('moveend', this.onBoundsChange.bind(this))
  }

  componentDidUpdate (prevProps, prevState) {
    // selected marker icon
    if (prevState.selected !== this.state.selected) {
      if (prevState.selected !== null) {
        this.markers[prevState.selected].setIcon(icon)
      }
      if (this.state.selected !== null) {
        this.markers[this.state.selected].setIcon(activeIcon)
      }
    }

    if (prevState.selected !== this.state.selected || prevState.filters !== this.state.filters) {
      // filter markers
      this.props.items.forEach((item, i) => {
        let marker = this.markers[i]
        if (!this.isInFilter(item)) {
          this.cluster.removeLayer(marker)
          this.selectedMarkers.removeLayer(marker)
        } else if (i === this.state.selected) {
          this.cluster.removeLayer(marker)
          // Removing a marker from the cluster resets its zIndexOffset,
          // thus the zIndexOffset of the selected marker has to be set
          // after it is removed from the cluster to rise it to the front.
          marker.setZIndexOffset(1000)
          this.selectedMarkers.addLayer(marker)
          console.log(marker)
        } else {
          this.selectedMarkers.removeLayer(marker)
          this.cluster.addLayer(marker)
          // Reset the markers default zIndexOffset.
          marker.setZIndexOffset(0)
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

  render () {
    return (
      <div className="map-list-combined">
        <div className="map-list-combined__map" ref={this.bindMap.bind(this)} />
        <ul className="u-list-reset map-list-combined__list" ref={this.bindList.bind(this)}>
          {
            this.props.items.map((item, i) => {
              if (this.isInFilter(item)) {
                let className = 'list-item'
                if (i === this.state.selected) {
                  className += ' selected'
                }

                return (
                  <li className={className} key={i}>{ item.title }</li>
                )
              }
            })
          }
        </ul>
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

    ReactDOM.render(<PlansMap items={items} attribution={attribution} baseurl={baseurl} bounds={bounds} />, element)
  })
}

$(init)
$(document).on('a4.embed.ready', init)
