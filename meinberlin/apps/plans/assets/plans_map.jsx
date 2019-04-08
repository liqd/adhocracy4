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
    let selectedDistrict = element.getAttribute('data-selected-district')
    let selectedTopic = element.getAttribute('data-selected-topic')
    let districts = JSON.parse(element.getAttribute('data-districts'))
    let organisations = JSON.parse(element.getAttribute('data-organisations'))
    let districtnames = JSON.parse(element.getAttribute('data-district-names'))
    let topicChoices = JSON.parse(element.getAttribute('data-topic-choices'))
    let token = element.getAttribute('data-token')
    let useVectorMap = element.getAttribute('data-use_vector_map')
    ReactDOM.render(<ListMapBox
      selectedDistrict={selectedDistrict}
      selectedTopic={selectedTopic}
      initialitems={items}
      attribution={attribution}
      baseurl={baseurl}
      token={token}
      useVectorMap={useVectorMap}
      bounds={bounds}
      organisations={organisations}
      districts={districts}
      districtnames={districtnames}
      topicChoices={topicChoices} />, element)
  })
}

$(init)
$(document).on('a4.embed.ready', init)
