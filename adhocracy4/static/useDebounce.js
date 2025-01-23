import { useEffect, useMemo, useRef } from 'react'
import debounce from 'lodash.debounce'

/**
 * A custom hook that returns a debounced callback function. A debounced function
 * means that it will wait for a certain amount of time before executing the
 * original function. So it will make sure that for certain events like typing
 * in an input field, the function is not executed too often.
 *
 * @param {function} callback - The callback function to be debounced.
 * @param {number} delay - The delay in milliseconds.
 * @returns {function} - The debounced callback function.
 */
const useDebounce = (callback, delay = 1000) => {
  const ref = useRef()

  useEffect(() => {
    ref.current = callback
  }, [callback])

  const debouncedCallback = useMemo(() => {
    const func = () => {
      ref.current?.()
    }

    return debounce(func, delay)
  }, [delay])

  return debouncedCallback
}

export default useDebounce
