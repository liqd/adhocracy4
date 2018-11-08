/* global django */
const React = require('react')
const ReactDOM = require('react-dom')
const $ = require('jquery')
const L = require('leaflet')
require('mapbox-gl-leaflet')

class PlansList extends React.Component {
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

  componentDidMount () {

  }

  componentDidUpdate (prevProps, prevState) {
    if (prevState.selected !== this.state.selected || prevState.filters !== this.state.filters) {
      // filter markers
      this.props.items.forEach((item, i) => {
        if (item.point !== '') {
          if (!this.isInFilter(item)) {
            this.setMarkerFiltered(i)
          } else if (i === this.state.selected) {
            this.setMarkerSelected(i, item)
          } else {
            this.setMarkerDefault(i, item)
          }
        }
      })
    }
  }

  renderListItem (item, i) {
    let itemClass = 'list-item list-item--squashed'
    if (i === this.state.selected) {
      itemClass += ' selected'
    }
    let statusClass = (item.participation_active === true) ? 'list-item__status--active' : 'list-item__status--inactive'
    return (
      <li className={itemClass} key={i} tabIndex="0">
        <div className="list-item__labels">
          {
            <span className="label label--secondary">{item.status_display}</span>
          } {item.district &&
            <span className="label"><i className="fas fa-map-marker-alt" aria-hidden="true" /> {item.district}</span>
          }
        </div>
        <h3 className="list-item__title"><a href={item.url}>{item.title}</a></h3>
        <div className="list-item__subtitle"><b>{django.gettext('Theme: ')}</b><span>{item.theme}</span></div>
        <div className="list-item__subtitle"><b>{django.gettext('Participation: ')}</b><span className={statusClass}>{item.participation_string}</span></div>
      </li>
    )
  }

  renderList () {
    let list = []
    this.props.items.forEach((item, i) => {
      list.push(this.renderListItem(item, i))
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
      <div className="map-list-combined__list" ref={this.bindList.bind(this)}>
        {this.renderList()}
      </div>
    )
  }
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

class ListMapBox extends React.Component {
  render () {
    return (
      <div className="map-list-combined">
        <div className="list-container">
          <PlansList key="content" items={this.props.items} />
        </div>
        <div className="map-container map-list-combined__map">
          <PlansMap key="content" items={this.props.items} bounds={this.props.bounds} districts={this.props.districts} baseurl={this.props.baseurl} districtnames={this.props.districtnames} />
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
    // ReactDOM.render(<PlansMap items={items} attribution={attribution} baseurl={baseurl} bounds={bounds} districts={districts} districtnames={districtnames} exportUrl={exportUrl} />, element)
    // ReactDOM.render(<PlansList items={items} attribution={attribution} baseurl={baseurl} bounds={bounds} districts={districts} districtnames={districtnames} exportUrl={exportUrl} />, element)
    ReactDOM.render(<ListMapBox items={items} attribution={attribution} baseurl={baseurl} bounds={bounds} districts={districts} districtnames={districtnames} exportUrl={exportUrl} />, element)
  })
}

$(init)
$(document).on('a4.embed.ready', init)
