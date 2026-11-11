// Behaviour for client side multi step forms (e.g. the idea submission form).
//
// Progressive enhancement: the whole form is rendered in the DOM, marking each
// logical section with `data-step-wizard-step`. Without JavaScript all sections
// stay visible and the form submits as a whole. With JavaScript only the active
// section is shown and the "Next" button validates the current section before
// advancing.

// Hidden inputs are barred from constraint validation and widgets with a
// hidden native control (e.g. the CKEditor source textarea) are synced before
// validation, so the remaining fields can be checked even when their step is
// not the active one.
function isValidatable (field) {
  return typeof field.checkValidity === 'function' && field.type !== 'hidden'
}

function firstInvalidField (step) {
  const fields = step.querySelectorAll('input, select, textarea')
  return Array.from(fields).find(function (field) {
    return isValidatable(field) && !field.checkValidity()
  })
}

// Rich text editors keep their content in a separate model and only copy it
// back to the underlying textarea on submit. Sync it before validating so a
// required editor is checked against what the user actually typed.
function syncRichTextEditors (container) {
  const editors = window.editors
  if (!editors) {
    return
  }
  Object.keys(editors).forEach(function (id) {
    const editor = editors[id]
    if (
      editor &&
      editor.sourceElement &&
      container.contains(editor.sourceElement) &&
      typeof editor.updateSourceElement === 'function'
    ) {
      editor.updateSourceElement()
    }
  })
}

function focusStep (step) {
  const field = step.querySelector(
    'input:not([type="hidden"]):not([type="file"]):not([disabled]), ' +
    'select:not([disabled]), textarea:not([disabled])'
  )
  if (field) {
    field.focus()
  }
}

function reportField (field) {
  if (!field) {
    return
  }
  // Widgets such as CKEditor hide the native control, so report the error on
  // the visible editor and focus it.
  const container = field.closest('.ck-editor-container')
  const editable = container
    ? container.querySelector('.ck-editor__editable')
    : null
  if (editable) {
    field.setAttribute('aria-invalid', 'true')
    editable.setAttribute('aria-invalid', 'true')
    editable.focus()
    return
  }
  // Widgets such as select2 hide the native control, so reporting validity may
  // fail because the element is not focusable. Swallow that and fall back to
  // focusing whatever is visible.
  try {
    field.reportValidity()
  } catch {
    field.focus()
  }
}

function clearInvalid (step) {
  step.querySelectorAll('[aria-invalid="true"]').forEach(function (field) {
    field.removeAttribute('aria-invalid')
  })
}

function initStepWizard (form) {
  if (form.dataset.stepWizardInitialized) {
    return
  }

  const steps = Array.from(form.querySelectorAll('[data-step-wizard-step]'))
  if (steps.length < 2) {
    return
  }

  form.dataset.stepWizardInitialized = 'true'
  form.classList.add('step-wizard')

  const progress = form.querySelector('[data-step-wizard-progress]')
  const status = form.querySelector('[data-step-wizard-status]')
  const backButton = form.querySelector('[data-step-wizard-back]')
  const nextButton = form.querySelector('[data-step-wizard-next]')
  const submitButton = form.querySelector('[data-step-wizard-submit]')

  const total = steps.length
  let current = 0
  let segments = []
  let summaryImageUrl = null

  // The number of rendered steps varies (optional steps may be omitted server
  // side), so build the progress segments from the actual steps.
  function buildProgress () {
    if (!progress) {
      return
    }
    progress.innerHTML = ''
    segments = []
    for (let index = 0; index < total; index++) {
      const segment = document.createElement('span')
      segment.className = 'step-wizard__segment'
      progress.appendChild(segment)
      segments.push(segment)
    }
  }

  function initialStep () {
    // After a server side validation error, jump to the first affected step.
    const errorIndex = steps.findIndex(function (step) {
      return step.querySelector('[role="alert"], .errorlist, [aria-invalid="true"]')
    })
    if (errorIndex > -1) {
      return errorIndex
    }
    const requested = parseInt(
      new URLSearchParams(window.location.search).get('step'),
      10
    )
    if (requested > 0 && requested <= total) {
      return requested - 1
    }
    return 0
  }

  function updateController () {
    if (backButton) {
      backButton.classList.toggle('d-none', current === 0)
    }
    if (nextButton) {
      nextButton.classList.toggle('d-none', current === total - 1)
    }
    if (submitButton) {
      submitButton.classList.toggle('d-none', current !== total - 1)
    }
  }

  function updateProgress () {
    segments.forEach(function (segment, index) {
      segment.classList.toggle('is-active', index <= current)
    })
    if (status) {
      const label = status.dataset.label || ''
      status.textContent = label
        .replace('%(current)s', String(current + 1))
        .replace('%(total)s', String(total))
    }
  }

  function stepOf (field) {
    return steps.findIndex(function (step) {
      return step.contains(field)
    })
  }

  function textFromHtml (html) {
    const container = document.createElement('div')
    container.innerHTML = html
    return (container.textContent || '').replace(/\s+/g, ' ').trim()
  }

  function labelText (form, input) {
    if (input.id) {
      const label = form.querySelector('label[for="' + input.id + '"]')
      if (label) {
        return label.textContent.trim()
      }
    }
    const parent = input.closest('label')
    return parent ? parent.textContent.trim() : input.value
  }

  function renderSummary () {
    const summary = form.querySelector('[data-step-wizard-summary]')
    if (!summary) {
      return
    }
    syncRichTextEditors(form)
    const labels = summary.dataset
    const rows = []
    const add = function (label, value, field) {
      if (value) {
        rows.push({ label: label, value: value, field: field })
      }
    }

    const pointLabel = form.querySelector('input[name="point_label"], #id_point_label')
    if (pointLabel) {
      add(labels.labelLocation, pointLabel.value.trim(), pointLabel)
    }

    const nameInput = form.querySelector('input[name="name"]')
    if (nameInput) {
      add(labels.labelTitle, nameInput.value.trim(), nameInput)
    }

    const description = form.querySelector('textarea[name="description"]')
    if (description) {
      const text = textFromHtml(description.value)
      add(
        labels.labelDescription,
        text.length > 120 ? text.slice(0, 117) + '…' : text,
        description
      )
    }

    const category = form.querySelector('select[name="category"]')
    if (category && category.value && category.selectedIndex > -1) {
      const option = category.options[category.selectedIndex]
      add(labels.labelCategory, option ? option.textContent.trim() : '', category)
    }

    const selectedLabels = Array.from(
      form.querySelectorAll('input[name="labels"]:checked')
    )
    if (selectedLabels.length) {
      add(
        labels.labelLabels,
        selectedLabels.map(function (input) { return labelText(form, input) }).join(', '),
        selectedLabels[0]
      )
    }

    const image = form.querySelector('input[name="image"]')
    if (image && image.files && image.files.length) {
      add(labels.labelImage, image.files[0].name, image)
    }

    summary.innerHTML = ''
    if (summaryImageUrl) {
      URL.revokeObjectURL(summaryImageUrl)
      summaryImageUrl = null
    }

    const imageInput = form.querySelector('input[name="image"]')
    if (imageInput && imageInput.files && imageInput.files.length) {
      summaryImageUrl = URL.createObjectURL(imageInput.files[0])
      const preview = document.createElement('img')
      preview.className = 'step-wizard__summary-image'
      preview.src = summaryImageUrl
      preview.alt = ''
      summary.appendChild(preview)
    }

    if (!rows.length) {
      return
    }
    const list = document.createElement('dl')
    list.className = 'step-wizard__summary-list'
    rows.forEach(function (row) {
      const item = document.createElement('div')
      item.className = 'step-wizard__summary-row'

      const term = document.createElement('dt')
      term.textContent = row.label

      const value = document.createElement('dd')
      const text = document.createElement('span')
      text.className = 'step-wizard__summary-value'
      text.textContent = row.value
      value.appendChild(text)

      const index = stepOf(row.field)
      if (index > -1) {
        const edit = document.createElement('button')
        edit.type = 'button'
        edit.className = 'step-wizard__summary-edit'
        edit.textContent = labels.labelEdit || 'Edit'
        edit.addEventListener('click', function () {
          goTo(index)
        })
        value.appendChild(edit)
      }

      item.appendChild(term)
      item.appendChild(value)
      list.appendChild(item)
    })
    summary.appendChild(list)
  }

  function render (moveFocus) {
    steps.forEach(function (step, index) {
      const active = index === current
      step.classList.toggle('d-none', !active)
    })
    updateController()
    updateProgress()
    if (current === total - 1) {
      renderSummary()
    }
    if (moveFocus) {
      focusStep(steps[current])
      // Let layout dependent widgets (e.g. the map) recalculate their size now
      // that the step is visible.
      window.requestAnimationFrame(function () {
        window.dispatchEvent(new Event('resize'))
      })
    }
  }

  function goTo (index) {
    current = Math.min(Math.max(index, 0), total - 1)
    render(true)
  }

  function advance () {
    syncRichTextEditors(steps[current])
    const invalid = firstInvalidField(steps[current])
    if (invalid) {
      reportField(invalid)
      return
    }
    clearInvalid(steps[current])
    goTo(current + 1)
  }

  if (nextButton) {
    nextButton.addEventListener('click', advance)
  }
  if (backButton) {
    backButton.addEventListener('click', function () {
      goTo(current - 1)
    })
  }

  // The form is rendered with `novalidate`, so validate all steps before
  // submitting and surface the first invalid one.
  form.addEventListener('submit', function (event) {
    // Enter on an intermediate step should advance instead of submitting the
    // whole form.
    if (current !== total - 1) {
      event.preventDefault()
      advance()
      return
    }
    syncRichTextEditors(form)
    for (let index = 0; index < total; index++) {
      const invalid = firstInvalidField(steps[index])
      if (invalid) {
        event.preventDefault()
        current = index
        render(true)
        reportField(invalid)
        return
      }
    }
  })

  buildProgress()
  current = initialStep()
  render(false)
}

function init () {
  document.querySelectorAll('form[data-step-wizard]').forEach(initStepWizard)
}

// Hide the inactive steps only after the browser had a chance to run the other
// DOMContentLoaded handlers. Map widgets, for instance, measure their container
// on init and render the wrong extent when it is already hidden.
function scheduleInit () {
  if (typeof window.requestAnimationFrame === 'function') {
    window.requestAnimationFrame(function () {
      init()
    })
  } else {
    window.setTimeout(init, 0)
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', scheduleInit, false)
} else {
  scheduleInit()
}

document.addEventListener('a4.embed.ready', scheduleInit, false)

export { initStepWizard }
