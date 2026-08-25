import type * as JQuery from 'jquery'

declare global {
  interface Window {
    jQuery?: typeof JQuery
    $?: typeof JQuery
    adhocracy4?: {
      getCurrentPath: () => string
    }
  }
}

export {}
