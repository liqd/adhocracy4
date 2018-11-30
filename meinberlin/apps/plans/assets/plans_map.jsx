const React = require('react')
const ReactDOM = require('react-dom')
const $ = require('jquery')
var ListMapBox = require('./ListMapBox')

const init = function () {
  $('[data-map="plans"]').each(function (i, element) {
    let items = JSON.parse(element.getAttribute('data-items'))
    let attribution = element.getAttribute('data-attribution')
    let baseurl = element.getAttribute('data-baseurl')
    let bounds = JSON.parse(element.getAttribute('data-bounds'))
    let districts = JSON.parse(element.getAttribute('data-districts'))
    let districtnames = JSON.parse(element.getAttribute('data-district-names'))
    let exportUrl = element.getAttribute('data-export-url')
    ReactDOM.render(<ListMapBox items={items} attribution={attribution} baseurl={baseurl} bounds={bounds} districts={districts} districtnames={districtnames} exportUrl={exportUrl} />, element)
  })
}

$(init)
$(document).on('a4.embed.ready', init)
