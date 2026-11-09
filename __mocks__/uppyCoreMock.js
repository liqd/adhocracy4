const uppy = {
  use: () => {},
  on: () => {},
  getPlugin: () => ({
    openModal: () => {},
    closeModal: () => {},
    stop: () => {}
  }),
  getFiles: () => [],
  removeFile: () => {},
  upload: () => Promise.resolve(),
  destroy: () => {}
}

const Uppy = function () {
  return uppy
}

module.exports = { __esModule: true, default: Uppy }
