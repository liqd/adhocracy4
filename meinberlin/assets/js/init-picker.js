import django from 'django'
import flatpickr from 'flatpickr'

function link (f0, f1) {
  const date = f0.selectedDates[0]
  if (date) {
    // if p0 has a date set that date as minDate for p1
    f1.set('minDate', f0.formatDate(date, f0.config.dateFormat))
  }
  f0.config.onChange.push((selectedDates, dateStr) => {
    // if date of p0 is changed adapt minDate for p1
    f1.set('minDate', dateStr)
  })
}

function linkDatePickers (flatpickrs) {
  // normal flatpickers
  const idStart = 'id_start_date_date'
  const idEnd = 'id_end_date_date'
  // (multi-)phase flatpickrs
  const phaseIds = [
    'id_phase_set-0-start_date_date',
    'id_phase_set-0-end_date_date',
    'id_phase_set-1-start_date_date',
    'id_phase_set-1-end_date_date',
    'id_phase_set-2-start_date_date',
    'id_phase_set-2-end_date_date'
  ]

  // link non-phase datepickers if exist
  const fStart = flatpickrs.get(idStart)
  const fEnd = flatpickrs.get(idEnd)
  if (fStart && fEnd) {
    link(fStart, fEnd)
  }

  // link phase datepickers if exist
  for (let i = 0; i < phaseIds.length - 1; i++) {
    if (flatpickrs.length <= i) {
      return
    }
    const p0 = flatpickrs.get(phaseIds[i])
    const p1 = flatpickrs.get(phaseIds[i + 1])
    if (p0 && p1) {
      link(p0, p1)
    }
  }
}

function initDatePicker () {
  const datepickers = document.querySelectorAll('.datepicker')
  const format = django.get_format('DATE_INPUT_FORMATS')[0].replaceAll('%', '')
  const flatpickrs = new Map()
  datepickers.forEach((e) => {
    e.classList.add('form-control')
    const f = flatpickr(e, { dateFormat: format })
    flatpickrs.set(e.id, f)
  })

  linkDatePickers(flatpickrs)

  const timepickers = document.querySelectorAll('.timepicker')

  timepickers.forEach((e) => {
    const f = flatpickr(e, {
      defaultHour: e.id.endsWith('start_date_time') ? '00' : '23',
      defaultMinute: e.id.endsWith('start_date_time') ? '00' : '59',
      dateFormat: 'H:i',
      enableTime: true,
      noCalendar: true,
      time_24hr: true
    })
    flatpickrs.set(e.id, f)
  })
}

document.addEventListener('DOMContentLoaded', initDatePicker, false)
