const React = require('react')
const ReactDOM = require('react-dom')
const $ = require('jquery')

class PlansMap extends React.Component {
  render () {
    return (
      <div className="map-list-combined">
        <div className="map-list-combined__map" />
        <ul className="u-list-reset map-list-combined__list">
          {
            this.props.items.map((item, i) => {
              let className = 'list-item'

              return (
                <li className={className} key={i}>{ item.title }</li>
              )
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
