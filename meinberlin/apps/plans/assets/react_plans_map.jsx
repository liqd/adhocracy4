import React from 'react'
import { createRoot } from 'react-dom/client'
import { CookiesProvider } from 'react-cookie'
import PlansListMapBox from './PlansListMapBox'

function init () {
  const plansMapBox = document.querySelectorAll('[data-map="plans"]')
  plansMapBox.forEach(el => {
    const projectApiUrl = el.getAttribute('data-projects-url')
    const extprojectApiUrl = el.getAttribute('data-extprojects-url')
    const privateprojectApiUrl = el.getAttribute('data-privateprojects-url')
    const plansApiUrl = el.getAttribute('data-plans-url')
    const attribution = el.getAttribute('data-attribution')
    const baseurl = el.getAttribute('data-baseurl')
    const bounds = JSON.parse(el.getAttribute('data-bounds'))
    const selectedDistrict = el.getAttribute('data-selected-district')
    const selectedTopic = el.getAttribute('data-selected-topic')
    const districts = JSON.parse(el.getAttribute('data-districts'))
    const organisations = JSON.parse(el.getAttribute('data-organisations'))
    const districtnames = JSON.parse(el.getAttribute('data-district-names'))
    const topicChoices = JSON.parse(el.getAttribute('data-topic-choices'))
    const mapboxToken = el.getAttribute('data-mapbox-token')
    const omtToken = el.getAttribute('data-omt-token')
    const useVectorMap = el.getAttribute('data-use_vector_map')
    const participationChoices = JSON.parse(el.getAttribute('data-participation-choices'))
    const root = createRoot(el)
    root.render(
      <React.StrictMode>
        <CookiesProvider>
          <PlansListMapBox
            selectedDistrict={selectedDistrict}
            selectedTopic={selectedTopic}
            projectApiUrl={projectApiUrl}
            extprojectApiUrl={extprojectApiUrl}
            privateprojectApiUrl={privateprojectApiUrl}
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
            participationChoices={participationChoices}
          />
        </CookiesProvider>
      </React.StrictMode>)
  })
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
