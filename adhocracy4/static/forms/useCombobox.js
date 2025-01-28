import { useCallback, useId, useMemo, useRef, useState } from 'react'
import { getLoopedIndex } from './AutoComplete'

function getTargets (choices, focusedIndex) {
  return {
    first: choices[0],
    last: choices[choices.length - 1],
    next: typeof focusedIndex === 'number' ? getLoopedIndex(choices, focusedIndex + 1) : null,
    prev: typeof focusedIndex === 'number' ? getLoopedIndex(choices, focusedIndex - 1) : null
  }
}

function toggleValue (value, values) {
  const shouldRemove = values.includes(value)
  let newValues = [...values, value]
  if (shouldRemove) {
    newValues = values.filter(item => item !== value)
  }
  return newValues
}

/**
 * A custom hook that provides accessibility and keyboard/event handling for combobox-like components.
 * This means it can be used for any select-like ui element. So, an autocomplete, a multiselect, etc.
 * Implements the WAI-ARIA Combobox Pattern (https://www.w3.org/WAI/ARIA/apg/patterns/combobox/).
 *
 * @param {Object} props - The configuration options for the combobox
 * @param {Array<{name: string, value: any}>} props.choices - Array of choice objects with name and value properties
 * @param {Array<any>} [props.values] - Array of selected values (for controlled components)
 * @param {any|Array<any>} [props.defaultValue] - Default selected value(s) (for uncontrolled components)
 * @param {Function} [props.onChange] - Callback function called when selection changes: (newValues: Array<any>) => void
 * @param {boolean} [props.isAutoComplete] - Whether the combobox is used for autocompletion
 * @param {boolean} [props.isMultiple] - Whether multiple values can be selected
 * @param {string} [props.search] - Search string for filtering choices
 *
 * @returns {Object} An object containing:
 * .comboboxAttrs - Props to spread on the combobox element including ARIA attributes
 * .listboxAttrs - Props to spread on the listbox element including ARIA attributes
 * .labelId - Generated ID for the label element
 * .activeItems - Currently selected items
 * .getChoicesAttr - Function to get props for individual choice elements
 * .opened - Whether the listbox is currently open
 *
 * @example
 * see adhocracy4/static/forms/AutoComplete.jsx
 */
const useCombobox = ({
  choices,
  values,
  defaultValue,
  onChange,
  isAutoComplete,
  isMultiple,
  search
}) => {
  const defaultValueArray = Array.isArray(defaultValue) ? defaultValue : [defaultValue]

  const listboxRef = useRef(null)
  const comboboxRef = useRef(null)
  const typed = useRef('')

  const [internalValue, setInternalValue] = useState(defaultValueArray)
  const [focused, setFocused] = useState(null)
  const [opened, setOpened] = useState(false)

  const containerId = useId()
  const labelId = useId()

  // Use values prop if provided (controlled), otherwise use internal state (uncontrolled)
  const active = useMemo(() => values ?? internalValue, [values, internalValue])

  const activeItems = choices.filter(choice => active.includes(choice.value))
  const focusedItem = choices.find((choice) => choice.value === focused)
  const focusedIndex = choices.findIndex(choice => choice.value === focused)
  const targets = getTargets(choices, focusedIndex)

  const toggleOption = useCallback((v) => {
    const newValues = isMultiple ? toggleValue(v, active) : [v]
    if (values === undefined) setInternalValue(newValues)
    if (onChange) onChange(newValues)
    if (!isMultiple) setOpened(false)
  }, [values, onChange, active])

  const onClick = useCallback(() => {
    if (!opened && targets.first) {
      setFocused(targets.first.value)
    }
    setOpened(!opened)
  }, [opened])

  const onBlur = useCallback((e) => {
    if (listboxRef.current?.contains(e.relatedTarget)) {
      setTimeout(() => comboboxRef.current?.focus(), 10)
      return
    }
    setOpened(false)
  }, [listboxRef])

  const getChoicesAttr = (choice) => ({
    active: active.includes(choice.value),
    focused: focusedItem?.value === choice.value,
    role: 'option',
    'aria-selected': active.includes(choice.value),
    onClick: () => {
      toggleOption(choice.value)
      setFocused(choice.value)
    },
    ref: focusedItem?.value === choice.value ? (node) => node?.scrollIntoView({ block: 'nearest' }) : null,
    tabIndex: -1
  })

  const onKeyDown = useCallback((e) => {
    const key = e.key
    switch (key) {
      case ' ':
        if (isAutoComplete) return
        e.preventDefault()
        if (!opened && targets.first) {
          setFocused(targets.first.value)
          setOpened(true)
        } else if (focused) {
          toggleOption(focused)
        } else {
          return
        }
        break
      case 'Enter':
        e.preventDefault()

        if (opened && typeof focused !== 'undefined') {
          toggleOption(focused)
        } else if (!opened) {
          setFocused(targets.first.value)
        }
        setOpened(!opened)
        break
      case 'Escape':
        setOpened(false)
        break
      case 'ArrowUp':
        e.preventDefault()
        if (targets.prev) {
          setFocused(targets.prev.value)
        }
        break
      case 'ArrowDown':
        e.preventDefault()
        if (targets.next) {
          setFocused(targets.next.value)
        }
        if (!opened) {
          if (targets.first) {
            setFocused(targets.first.value)
          }
          setOpened(true)
        }
        break
      case 'Home':
        e.preventDefault()
        setFocused(targets.first.value)
        break
      case 'End':
        e.preventDefault()
        setFocused(targets.last.value)
        break
    }
    if (key.length === 1 && !isAutoComplete) {
      typed.current += key
      const filtered = choices.filter(choice => choice.name.toLowerCase().startsWith(typed.current.toLowerCase()))
      if (filtered.length) {
        setFocused(filtered[0].value)
      }
      setTimeout(() => { typed.current = '' }, 200)
    }
  }, [focused, opened, targets, choices, isAutoComplete])

  return {
    comboboxAttrs: {
      onClick,
      onBlur,
      onKeyDown,
      tabIndex: 0,
      'aria-haspopup': 'true',
      'aria-expanded': opened,
      'aria-activedescendant': focusedItem?.value,
      'aria-labelledby': labelId,
      'aria-controls': containerId,
      role: 'combobox',
      ref: comboboxRef
    },
    listboxAttrs: {
      role: 'listbox',
      'aria-multiselectable': 'true',
      ref: listboxRef,
      id: containerId
    },
    labelId,
    activeItems,
    getChoicesAttr,
    opened
  }
}

export default useCombobox
