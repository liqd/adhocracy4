import { Swiper } from 'swiper'
/* eslint import/no-unresolved: [2, { ignore: ['swiper/modules'] }] */
import { Pagination, A11y } from 'swiper/modules'
import django from 'django'

function createSwiper (params) {
  const { rootElement, options } = params
  return new Swiper(rootElement, options)
}

// find index for given identifier in slide
// possible identifiers: active, upcoming
function getIndexOf (identifier, slides) {
  return Array.from(slides).findIndex(slide => {
    return slide.querySelector('#' + identifier)
  })
}

// create specific phase swiper
function createPhaseSwiper () {
  // config contains container/root element's name
  // and all settings, which are needed (see swiper docs)
  const config = {
    rootElement: '.swiper-phases',
    options: {
      modules: [A11y, Pagination],
      a11y: {
        containerMessage:
          django.gettext('Slider to go back and forth between phases.'),
        paginationBulletMessage:
          django.gettext('Go to slide {{index}}')
      },
      pagination: {
        el: '.swiper-pagination',
        clickable: true,
        bulletElement: 'div'
      }
    }
  }
  const phaseSwiper = createSwiper(config)

  // following part is to set initial slide
  // FIXME: it is not the right location to invoke the following;
  // because double logic (similar as in template), better to set
  // flag `initialSlide` in config on creation
  const activeSlideIndex = getIndexOf('active-phase', phaseSwiper.slides)
  const upcomingSlideIndex = getIndexOf('upcoming-phase', phaseSwiper.slides)

  if (activeSlideIndex !== -1) {
    phaseSwiper.slideTo(activeSlideIndex)
  } else if (upcomingSlideIndex !== -1) {
    phaseSwiper.slideTo(upcomingSlideIndex)
  } else {
    const lastFinishedSlideIndex = phaseSwiper.slides.length - 1
    phaseSwiper.slideTo(lastFinishedSlideIndex)
  }
}

(function () {
  // Call swiper initialization if swiper element found in DOM
  // const hasPhaseSwiper = document.querySelector('.swiper-phases')
  createPhaseSwiper()
})()
