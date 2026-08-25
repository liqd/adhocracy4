declare module 'django' {
  export function gettext(text: string): string
  export function pgettext(context: string, text: string): string
  export function ngettext(singular: string, plural: string, count: number): string
  export function interpolate(fmt: string, data: string[] | string | object | number, named?: boolean): string
}
