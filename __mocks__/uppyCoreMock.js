const createUppyMock = () => {
  const handlers = {}
  const plugins = {}

  return {
    use: () => {},
    on: (event, handler) => {
      handlers[event] = handler
    },
    emit: (event, ...args) => {
      if (handlers[event]) {
        return handlers[event](...args)
      }
      return undefined
    },
    getPlugin: (name) => {
      if (!plugins[name]) {
        plugins[name] = {
          openModal: jest.fn(),
          closeModal: jest.fn(),
          stop: jest.fn()
        }
      }
      return plugins[name]
    },
    getFiles: () => [],
    removeFile: () => {},
    upload: () => Promise.resolve(),
    destroy: () => {}
  }
}

const Uppy = jest.fn(() => createUppyMock())

module.exports = { __esModule: true, default: Uppy }
