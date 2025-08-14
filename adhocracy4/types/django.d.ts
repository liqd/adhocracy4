// django.d.ts
declare module 'django' {
  interface Django {
    /**
     * Translate the given string
     * @param text The text to translate
     */
    gettext(text: string): string;

    /**
     * Pluralize a string based on a count
     * @param singular The singular form
     * @param plural The plural form
     * @param count The number to determine pluralization
     */
    ngettext(singular: string, plural: string, count: number): string;

    /**
     * Translate a string with context
     * @param context Context marker for the text
     * @param text The text to translate
     */
    pgettext(context: string, text: string): string;

    /**
     * Pluralize a string with context
     * @param context Context marker for the text
     * @param singular The singular form
     * @param plural The plural form
     * @param count The number to determine pluralization
     */
    npgettext?(context: string, singular: string, plural: string, count: number): string;

    /**
     * String interpolation (optional - if you use it)
     * @param fmt The format string
     * @param args The arguments to interpolate
     */
    interpolate?(fmt: string, args: any, named?: boolean): string;
  }

  const django: Django;
  export default django;
}