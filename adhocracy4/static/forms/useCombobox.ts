import { useCallback, useId, useMemo, useRef, useState } from 'react'
import type { FocusEvent, KeyboardEvent, MouseEvent as ReactMouseEvent } from 'react'
import { getLoopedIndex } from './AutoComplete'

interface Choice<T = string> {
  name: string
  value: T
}

interface UseComboboxProps<T = string> {
  choices: Choice<T>[]
  values?: T[]
  defaultValue?: T | T[]
  onChange?: (newValues: T[]) => void
  isAutoComplete?: boolean
  isMultiple?: boolean
  search?: string
}

export interface ChoiceAttributes {
  active: boolean
  focused: boolean
  role: string
  id: string
  'aria-selected': boolean
  onClick: () => void
  ref: ((node: HTMLElement | null) => void) | null
  tabIndex: number
}

function getTargets<T> (choices: Choice<T>[], focusedIndex: number | null) {
  return {
    first: choices[0],
    last: choices[choices.length - 1],
    next: typeof focusedIndex === 'number' ? getLoopedIndex(choices, focusedIndex + 1) : null,
    prev: typeof focusedIndex === 'number' ? getLoopedIndex(choices, focusedIndex - 1) : null
  }
}

function toggleValue<T> (value: T, values: T[]) {
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
 */
const useCombobox = <T = string> ({
  choices,
  values,
  defaultValue,
  onChange,
  isAutoComplete,
  isMultiple,
  search: _search
}: UseComboboxProps<T>) => {
  const defaultValueArray = Array.isArray(defaultValue)
    ? defaultValue
    : defaultValue !== undefined
      ? [defaultValue]
      : []

  const listboxRef = useRef<HTMLUListElement>(null)
  const comboboxRef = useRef<HTMLDivElement>(null)
  const typed = useRef('')

  const [internalValue, setInternalValue] = useState<T[]>(defaultValueArray)
  const [focused, setFocused] = useState<T | null>(null)
  const [opened, setOpened] = useState(false)

  const containerId = useId()
  const labelId = useId()

  // Use values prop if provided (controlled), otherwise use internal state (uncontrolled)
  const active = useMemo(() => values ?? internalValue, [values, internalValue])

  const activeItems = choices.filter(choice => active.includes(choice.value))
  const focusedItem = choices.find((choice) => choice.value === focused)
  const focusedIndex = choices.findIndex(choice => choice.value === focused)
  const targets = getTargets(choices, focusedIndex === -1 ? null : focusedIndex)

  const toggleOption = useCallback((v: T) => {
    const newValues = isMultiple ? toggleValue(v, active) : [v]
    if (values === undefined) setInternalValue(newValues)
    if (onChange) onChange(newValues)
    if (!isMultiple) setOpened(false)
  }, [values, onChange, active, isMultiple])

  const onClick = useCallback(() => {
    if (!opened && targets.first) {
      setFocused(targets.first.value)
    }
    setOpened(!opened)
  }, [opened, targets])

  const onBlur = useCallback((e: FocusEvent) => {
    const related = e.relatedTarget as Node | null
    if (listboxRef.current?.contains(related)) {
      setTimeout(() => comboboxRef.current?.focus(), 10)
      return
    }
    setOpened(false)
  }, [listboxRef])

  const onMouseDown = useCallback((e: ReactMouseEvent) => {
    e.preventDefault()
  }, [])

  const getFocusedId = () => {
    if (!focusedItem) return undefined
    const index = choices.findIndex(c => c.value === focusedItem.value)
    return index !== -1 ? `${containerId}-option-${index}` : undefined
  }

  const getChoicesAttr = (choice: Choice<T>, index?: number): ChoiceAttributes => ({
    active: active.includes(choice.value),
    focused: focusedItem?.value === choice.value,
    role: 'option',
    id: `${containerId}-option-${index}`,
    'aria-selected': active.includes(choice.value),
    onClick: () => {
      toggleOption(choice.value)
      setFocused(choice.value)
    },
    ref: focusedItem?.value === choice.value ? (node: HTMLElement | null) => node?.scrollIntoView({ block: 'nearest' }) : null,
    tabIndex: -1
  })

  const onKeyDown = useCallback((e: KeyboardEvent) => {
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

        if (opened && focused !== null) {
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
  }, [focused, opened, targets, choices, isAutoComplete, toggleOption])

  return {
    comboboxAttrs: {
      onClick,
      onBlur,
      onKeyDown,
      tabIndex: 0,
      'aria-haspopup': 'true',
      'aria-expanded': opened,
      'aria-activedescendant': getFocusedId(),
      'aria-labelledby': labelId,
      'aria-controls': containerId,
      role: 'combobox',
      ref: comboboxRef
    } as any,
    listboxAttrs: {
      role: 'listbox',
      'aria-multiselectable': 'true',
      ref: listboxRef as any,
      id: containerId,
      'aria-labelledby': labelId,
      onMouseDown
    } as any,
    labelId,
    activeItems,
    getChoicesAttr: getChoicesAttr as any,
    opened
  }
}

export default useCombobox
