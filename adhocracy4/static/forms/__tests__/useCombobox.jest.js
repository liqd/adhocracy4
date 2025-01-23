import { renderHook, act } from '@testing-library/react'
import useCombobox from '../useCombobox'

const mockChoices = [
  { value: '1', name: 'Option 1' },
  { value: '2', name: 'Option 2' },
  { value: '3', name: 'Option 3' }
]

const defaultProps = {
  choices: mockChoices,
  values: undefined,
  defaultValue: [],
  onChange: jest.fn(),
  isAutoComplete: false,
  isMultiple: false,
  search: ''
}

describe('useCombobox', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  test('initializes with default values', () => {
    const { result } = renderHook(() => useCombobox(defaultProps))

    expect(result.current.opened).toBe(false)
    expect(result.current.activeItems).toEqual([])
    expect(result.current.labelId).toBeTruthy()
    expect(result.current.comboboxAttrs['aria-expanded']).toBe(false)
  })

  test('toggles dropdown on click', () => {
    const { result } = renderHook(() => useCombobox(defaultProps))

    act(() => {
      result.current.comboboxAttrs.onClick()
    })

    expect(result.current.opened).toBe(true)
    expect(result.current.comboboxAttrs['aria-expanded']).toBe(true)
  })

  test('handles keyboard navigation', () => {
    const { result } = renderHook(() => useCombobox(defaultProps))

    act(() => {
      result.current.comboboxAttrs.onClick()
    })
    expect(result.current.comboboxAttrs['aria-activedescendant']).toBe('1')

    act(() => {
      result.current.comboboxAttrs.onKeyDown({ key: 'ArrowDown', preventDefault: jest.fn() })
    })
    expect(result.current.comboboxAttrs['aria-activedescendant']).toBe('2')

    act(() => {
      result.current.comboboxAttrs.onKeyDown({ key: 'ArrowDown', preventDefault: jest.fn() })
    })
    expect(result.current.comboboxAttrs['aria-activedescendant']).toBe('3')

    act(() => {
      result.current.comboboxAttrs.onKeyDown({ key: 'ArrowUp', preventDefault: jest.fn() })
    })
    expect(result.current.comboboxAttrs['aria-activedescendant']).toBe('2')
  })

  test('handles multiple selection', () => {
    const multipleProps = {
      ...defaultProps,
      isMultiple: true
    }

    const { result } = renderHook(() => useCombobox(multipleProps))

    // Select first option
    act(() => {
      const choiceAttrs = result.current.getChoicesAttr(mockChoices[0])
      choiceAttrs.onClick()
    })

    expect(result.current.activeItems).toHaveLength(1)
    expect(result.current.activeItems[0]).toEqual(mockChoices[0])

    // Select second option
    act(() => {
      const choiceAttrs = result.current.getChoicesAttr(mockChoices[1])
      choiceAttrs.onClick()
    })

    expect(result.current.activeItems).toHaveLength(2)
    expect(result.current.activeItems).toEqual([mockChoices[0], mockChoices[1]])
  })

  test('handles single selection', () => {
    const { result } = renderHook(() => useCombobox(defaultProps))

    // Select first option
    act(() => {
      const choiceAttrs = result.current.getChoicesAttr(mockChoices[0])
      choiceAttrs.onClick()
    })

    expect(result.current.activeItems).toHaveLength(1)
    expect(result.current.activeItems[0]).toBe(mockChoices[0])

    // Select second option (should replace first)
    act(() => {
      const choiceAttrs = result.current.getChoicesAttr(mockChoices[1])
      choiceAttrs.onClick()
    })

    expect(result.current.activeItems).toHaveLength(1)
    expect(result.current.activeItems[0]).toBe(mockChoices[1])
  })

  test('closes on escape key', () => {
    const { result } = renderHook(() => useCombobox(defaultProps))

    // Open dropdown
    act(() => {
      result.current.comboboxAttrs.onClick()
    })

    expect(result.current.opened).toBe(true)

    // Press escape
    act(() => {
      result.current.comboboxAttrs.onKeyDown({ key: 'Escape' })
    })

    expect(result.current.opened).toBe(false)
  })

  test('handles controlled values', () => {
    const controlledProps = {
      ...defaultProps,
      values: ['1']
    }

    const { result } = renderHook(() => useCombobox(controlledProps))

    expect(result.current.activeItems).toHaveLength(1)
    expect(result.current.activeItems[0]).toBe(mockChoices[0])
  })

  test('handles type-to-select', () => {
    const { result } = renderHook(() => useCombobox(defaultProps))

    act(() => {
      result.current.comboboxAttrs.onKeyDown({ key: 'O', length: 1 })
    })

    expect(result.current.comboboxAttrs['aria-activedescendant']).toBe('1')
  })

  test('handles Home and End keys', () => {
    const { result } = renderHook(() => useCombobox(defaultProps))

    act(() => {
      result.current.comboboxAttrs.onKeyDown({ key: 'End', preventDefault: jest.fn() })
    })
    expect(result.current.comboboxAttrs['aria-activedescendant']).toBe('3')

    act(() => {
      result.current.comboboxAttrs.onKeyDown({ key: 'Home', preventDefault: jest.fn() })
    })
    expect(result.current.comboboxAttrs['aria-activedescendant']).toBe('1')
  })

  test('calls onChange when selection changes', () => {
    const onChange = jest.fn()
    const propsWithOnChange = {
      ...defaultProps,
      onChange
    }

    const { result } = renderHook(() => useCombobox(propsWithOnChange))

    act(() => {
      const choiceAttrs = result.current.getChoicesAttr(mockChoices[0])
      choiceAttrs.onClick()
    })

    expect(onChange).toHaveBeenCalledWith(['1'])
  })
})

describe('useCombobox accessibility', () => {
  test('provides correct ARIA attributes', () => {
    const { result } = renderHook(() => useCombobox(defaultProps))

    expect(result.current.comboboxAttrs['aria-haspopup']).toBe('true')
    expect(result.current.listboxAttrs['aria-multiselectable']).toBe('true')
    expect(result.current.listboxAttrs.role).toBe('listbox')
    expect(result.current.comboboxAttrs.role).toBe('combobox')
  })

  test('handles focus management correctly', () => {
    const { result } = renderHook(() => useCombobox(defaultProps))
    const mockEvent = {
      relatedTarget: null
    }

    act(() => {
      result.current.comboboxAttrs.onBlur(mockEvent)
    })

    expect(result.current.opened).toBe(false)
  })
})

describe('useCombobox with autoComplete', () => {
  test('handles space key differently in autoComplete mode', () => {
    const autoCompleteProps = {
      ...defaultProps,
      isAutoComplete: true
    }

    const { result } = renderHook(() => useCombobox(autoCompleteProps))

    act(() => {
      result.current.comboboxAttrs.onKeyDown({
        key: ' ',
        preventDefault: jest.fn()
      })
    })

    // Space should not trigger option selection in autoComplete mode
    expect(result.current.opened).toBe(false)
  })
})
