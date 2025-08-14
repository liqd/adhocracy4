import { RefObject, useCallback, useId, useMemo, useRef, useState } from 'react'
import Choice from '../../types/choice'

interface UseComboboxProps<T> {
  choices: Choice<T>[];
  values?: T[];
  defaultValue?: T | T[];
  onChange?: (newValues: T[]) => void;
  isAutoComplete?: boolean;
  isMultiple?: boolean;
  search?: string;
}

interface Targets<T> {
  first: Choice<T> | undefined;
  last: Choice<T> | undefined;
  next: Choice<T> | null;
  prev: Choice<T> | null;
}

interface ComboboxAttrs {
  onClick: () => void;
  onBlur: (e: React.FocusEvent) => void;
  onKeyDown: (e: React.KeyboardEvent) => void;
  tabIndex: number;
  'aria-haspopup': 'true';
  'aria-expanded': boolean;
  'aria-activedescendant': any;
  'aria-labelledby': string;
  'aria-controls': string;
  role: 'combobox';
  ref: React.RefObject<HTMLInputElement>;
}

interface ListboxAttrs {
  role: 'listbox';
  'aria-multiselectable': 'true';
  ref: React.RefObject<HTMLUListElement>;
  id: string;
  onMouseDown: (e: React.MouseEvent) => void;
}

interface UseComboboxReturn<T> {
  comboboxAttrs: ComboboxAttrs;
  listboxAttrs: ListboxAttrs;
  labelId: string;
  activeItems: Choice<T>[];
  getChoicesAttr: any;
  opened: boolean;
}

/*
 * Returns the item at the given index in an array, wrapping around
 * if index is out of bounds.
 */
const getLoopedIndex = <T, >(array: T[], index: number): T => {
  const length = array.length
  if (length === 0) throw new Error('Cannot get looped index of empty array')
  const wrappedIndex = ((index % length) + length) % length
  return array[wrappedIndex]
}

function getTargets<T> (choices: Choice<T>[], focusedIndex: number): Targets<T> {
  if (choices.length === 0) {
    return {
      first: undefined,
      last: undefined,
      next: null,
      prev: null
    }
  }

  return {
    first: choices[0],
    last: choices[choices.length - 1],
    next: typeof focusedIndex === 'number' ? getLoopedIndex(choices, focusedIndex + 1) : null,
    prev: typeof focusedIndex === 'number' ? getLoopedIndex(choices, focusedIndex - 1) : null
  }
}

function toggleValue<T> (value: T, values: T[]): T[] {
  const shouldRemove = values.includes(value)
  let newValues = [...values, value]
  if (shouldRemove) {
    newValues = values.filter((item) => item !== value)
  }
  return newValues
}

const useCombobox = <T, >({
  choices,
  values,
  defaultValue,
  onChange,
  isAutoComplete = false,
  isMultiple = false
}: UseComboboxProps<T>): UseComboboxReturn<T> => {
  const defaultValueArray = Array.isArray(defaultValue) ? defaultValue : defaultValue !== undefined ? [defaultValue] : []

  const listboxRef = useRef<HTMLElement>(null)
  const comboboxRef = useRef<HTMLLIElement>(null)
  const typed = useRef<string>('')

  const [internalValue, setInternalValue] = useState<T[]>(defaultValueArray)
  const [focused, setFocused] = useState<T | null>(null)
  const [opened, setOpened] = useState(false)

  const containerId = useId()
  const labelId = useId()

  const active = useMemo(() => values ?? internalValue, [values, internalValue])
  const activeItems = useMemo(() => choices.filter((choice) => active.includes(choice.value)), [choices, active])
  const focusedItem = useMemo(() => choices.find((choice) => choice.value === focused), [choices, focused])
  const focusedIndex = useMemo(() => choices.findIndex((choice) => choice.value === focused), [choices, focused])
  const targets = useMemo(() => getTargets(choices, focusedIndex), [choices, focusedIndex])

  const toggleOption = useCallback(
    (v: T) => {
      const newValues = isMultiple ? toggleValue(v, active) : [v]
      if (values === undefined) setInternalValue(newValues)
      onChange?.(newValues)
      if (!isMultiple) setOpened(false)
    },
    [values, onChange, active, isMultiple]
  )

  const onClick = useCallback(() => {
    if (!opened && targets.first) {
      setFocused(targets.first.value)
    }
    setOpened(!opened)
  }, [opened, targets.first])

  const onBlur = useCallback(
    (e: React.FocusEvent) => {
      if (listboxRef.current?.contains(e.relatedTarget as Node)) {
        setTimeout(() => comboboxRef.current?.focus(), 10)
        return
      }
      setOpened(false)
    },
    [listboxRef]
  )

  const onMouseDown = useCallback((e: React.MouseEvent) => {
    e.preventDefault()
  }, [])

  const getChoicesAttr = useCallback(
    (choice: Choice<T>) => ({
      active: active.includes(choice.value),
      focused: focusedItem?.value === choice.value,
      role: 'option' as const,
      'aria-selected': active.includes(choice.value),
      onClick: () => {
        toggleOption(choice.value)
        setFocused(choice.value)
      },
      ref: (node: HTMLElement | null) => {
        if (focusedItem?.value === choice.value) {
          node?.scrollIntoView({ block: 'nearest' })
        }
      },
      tabIndex: -1
    }),
    [active, focusedItem, toggleOption]
  )

  const onKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
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
          if (opened && focused !== undefined && focused !== null) {
            toggleOption(focused)
          } else if (!opened && targets.first) {
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
          if (!opened && targets.first) {
            setFocused(targets.first.value)
            setOpened(true)
          }
          break
        case 'Home':
          e.preventDefault()
          if (targets.first) {
            setFocused(targets.first.value)
          }
          break
        case 'End':
          e.preventDefault()
          if (targets.last) {
            setFocused(targets.last.value)
          }
          break
      }

      if (key.length === 1 && !isAutoComplete) {
        typed.current += key
        const filtered = choices.filter((choice) =>
          choice.name.toLowerCase().startsWith(typed.current.toLowerCase())
        )
        if (filtered.length) {
          setFocused(filtered[0].value)
        }
        setTimeout(() => {
          typed.current = ''
        }, 200)
      }
    },
    [focused, opened, targets, choices, isAutoComplete, toggleOption]
  )

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
      ref: comboboxRef as unknown as RefObject<HTMLInputElement>
    },
    listboxAttrs: {
      role: 'listbox',
      'aria-multiselectable': 'true',
      ref: listboxRef as unknown as RefObject<HTMLUListElement>,
      id: containerId,
      onMouseDown
    },
    labelId,
    activeItems,
    getChoicesAttr,
    opened
  }
}

export default useCombobox
