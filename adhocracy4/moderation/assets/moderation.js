/* Moderation dashboard widgets. */
import django from 'django'

document.addEventListener('DOMContentLoaded', function () {
  const feedbackDialog = document.getElementById('moderation-feedback-dialog')

  document.body.addEventListener('click', function (event) {
    const trigger = event.target.closest('[data-moderation-image]')
    if (!trigger) {
      return
    }

    const item = trigger.closest('.moderation-item')
    const dialog =
      (item && item.querySelector('dialog')) ||
      document.getElementById('moderation-image-dialog')
    if (!dialog || typeof dialog.showModal !== 'function') {
      return
    }

    event.preventDefault()
    const image = dialog.querySelector('img')
    image.src = trigger.getAttribute('data-moderation-image')
    dialog.showModal()

    dialog.onclick = function (dialogEvent) {
      if (dialogEvent.target === dialog) {
        dialog.close()
      }
    }
  })

  document.body.addEventListener('click', function (event) {
    const closeButton = event.target.closest('[data-moderation-dialog-close]')
    if (closeButton) {
      const dialog = closeButton.closest('dialog')
      if (dialog) {
        dialog.close()
      }
    }
  })

  if (feedbackDialog) {
    feedbackDialog.addEventListener('click', function (event) {
      if (event.target === feedbackDialog) {
        feedbackDialog.close()
      }
    })
  }

  document.addEventListener('click', function (event) {
    document
      .querySelectorAll('details.moderation-item__menu[open], details.moderation-card__menu[open]')
      .forEach(function (menu) {
        if (!menu.contains(event.target)) {
          menu.open = false
        }
      })
  })

  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape') {
      return
    }
    document
      .querySelectorAll('details.moderation-item__menu[open], details.moderation-card__menu[open]')
      .forEach(function (menu) {
        menu.open = false
      })
  })

  document.addEventListener('change', function (event) {
    const form = event.target.closest('form[data-moderation-auto-submit]')
    if (!form || event.target.tagName !== 'SELECT') {
      return
    }
    if (typeof form.requestSubmit === 'function') {
      form.requestSubmit()
    } else {
      form.submit()
    }
  })

  document.body.addEventListener('click', function (event) {
    const toggle = event.target.closest('[data-moderation-text-toggle]')
    if (!toggle) {
      return
    }
    const card = toggle.closest('.moderation-card')
    const shortText = card && card.querySelector('.moderation-card__text-short')
    const fullText = card && card.querySelector('.moderation-card__text-full')
    if (!shortText || !fullText) {
      return
    }
    const expanded = toggle.getAttribute('aria-expanded') === 'true'
    toggle.setAttribute('aria-expanded', expanded ? 'false' : 'true')
    shortText.hidden = !expanded
    fullText.hidden = expanded
  })

  document.addEventListener('click', function (event) {
    const tab = event.target.closest('.moderation-tabs .moderation-tab')
    if (!tab) {
      return
    }
    activateTab(tab.closest('.moderation-tabs'), tabState(tab))
  })

  window.addEventListener('popstate', function () {
    const params = new URLSearchParams(window.location.search)
    document.querySelectorAll('.moderation-tabs').forEach(function (tabs) {
      activateTab(tabs, params.get('state') || 'all')
    })
  })

  document.body.addEventListener('htmx:afterSwap', function (event) {
    const target = event.detail.target
    if (!target) {
      return
    }

    if (target.id === 'moderation-feedback-dialog-body' && feedbackDialog) {
      if (!feedbackDialog.open) {
        feedbackDialog.showModal()
      }
      return
    }

    if (target.id === 'moderation-items') {
      announce(django.gettext('The list was updated.'))
    }
  })

  document.body.addEventListener('htmx:beforeRequest', function (event) {
    const form = getFeedbackForm(event.detail && event.detail.elt)
    if (!form) {
      return
    }
    const button = form.querySelector('[type="submit"]')
    if (button) {
      button.disabled = true
      button.setAttribute('aria-disabled', 'true')
    }
  })

  document.body.addEventListener('htmx:afterRequest', function (event) {
    const form = getFeedbackForm(event.detail && event.detail.elt)
    if (!form) {
      return
    }
    const button = form.querySelector('[type="submit"]')
    if (button) {
      button.disabled = false
      button.removeAttribute('aria-disabled')
    }
    const changed = event.detail && event.detail.xhr &&
      event.detail.xhr.getResponseHeader('HX-Retarget')
    if (changed && feedbackDialog && feedbackDialog.open) {
      feedbackDialog.close()
    }
  })

  document.body.addEventListener('moderationItemUpdated', function (event) {
    announce(event.detail && event.detail.message)
  })

  document.body.addEventListener('moderationFeedbackSaved', function (event) {
    if (feedbackDialog && feedbackDialog.open) {
      feedbackDialog.close()
    }
    if (event.detail && event.detail.itemId) {
      window.setTimeout(function () {
        const item = document.getElementById(event.detail.itemId)
        const button =
          item && (item.querySelector('.moderation-item__menu-button') || item.querySelector('.moderation-card__menu-button'))
        if (button) {
          button.focus()
        } else if (item) {
          item.setAttribute('tabindex', '-1')
          item.focus()
        }
      }, 0)
    }
    announce(event.detail && event.detail.message)
  })
})

function tabState (tab) {
  const url = new URL(tab.getAttribute('href'), window.location.origin)
  return url.searchParams.get('state') || 'all'
}

function activateTab (tabs, state) {
  tabs.querySelectorAll('.moderation-tab').forEach(function (tab) {
    const active = tabState(tab) === state
    tab.classList.toggle('moderation-tab--active', active)
    if (active) {
      tab.setAttribute('aria-current', 'page')
    } else {
      tab.removeAttribute('aria-current')
    }
  })
}

function getFeedbackForm (element) {
  if (!element || typeof element.closest !== 'function') {
    return null
  }
  return element.closest('.moderation-feedback-form')
}

function announce (message) {
  const status = document.getElementById('moderation-status')
  if (status && message) {
    status.textContent = message
  }
}
