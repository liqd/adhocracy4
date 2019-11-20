import React from 'react'
import ReactDOM from 'react-dom'
import { CookiesProvider } from 'react-cookie'
import ListMapBox from './ListMapBox'

const init = function () {
  $('[data-map="plans"]').each(function (i, element) {
    const projectApiUrl = element.getAttribute('data-projects-url')
    const containersApiUrl = element.getAttribute('data-containers-url')
    const extprojectApiUrl = element.getAttribute('data-extprojects-url')
    const plansApiUrl = element.getAttribute('data-plans-url')
    const attribution = element.getAttribute('data-attribution')
    const baseurl = element.getAttribute('data-baseurl')
    const bounds = JSON.parse(element.getAttribute('data-bounds'))
    const selectedDistrict = element.getAttribute('data-selected-district')
    const selectedTopic = element.getAttribute('data-selected-topic')
    const districts = JSON.parse(element.getAttribute('data-districts'))
    const organisations = JSON.parse(element.getAttribute('data-organisations'))
    const districtnames = JSON.parse(element.getAttribute('data-district-names'))
    const topicChoices = JSON.parse(element.getAttribute('data-topic-choices'))
    const mapboxToken = element.getAttribute('data-mapbox-token')
    const omtToken = element.getAttribute('data-omt-token')
    const useVectorMap = element.getAttribute('data-use_vector_map')
    ReactDOM.render(
      <CookiesProvider>
        <ListMapBox
          selectedDistrict={selectedDistrict}
          selectedTopic={selectedTopic}
          projectApiUrl={projectApiUrl}
          containersApiUrl={containersApiUrl}
          extprojectApiUrl={extprojectApiUrl}
          plansApiUrl={plansApiUrl}
          attribution={attribution}
          baseurl={baseurl}
          mapboxToken={mapboxToken}
          omtToken={omtToken}
          useVectorMap={useVectorMap}
          bounds={bounds}
          organisations={organisations}
          districts={districts}
          districtnames={districtnames}
          topicChoices={topicChoices}
        />
      </CookiesProvider>,
      element)
  })
}

$(init)
$(document).on('a4.embed.ready', init)
