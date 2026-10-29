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
    const dialog = item && item.querySelector('dialog')
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
      .querySelectorAll('details.moderation-item__menu[open]')
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
      .querySelectorAll('details.moderation-item__menu[open]')
      .forEach(function (menu) {
        menu.open = false
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
          item && item.querySelector('.moderation-item__menu-button')
        if (button) {
          button.focus()
        }
      }, 0)
    }
    announce(event.detail && event.detail.message)
  })
})

function announce (message) {
  const status = document.getElementById('moderation-status')
  if (status && message) {
    status.textContent = message
  }
}
