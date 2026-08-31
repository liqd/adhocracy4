declare module 'file-saver' {
  export function saveAs(data: Blob | string, filename?: string, options?: any): void
  export const saveAs: typeof saveAs
}

declare module 'shpjs' {
  function shp(base: any): Promise<any>
  export default shp
}