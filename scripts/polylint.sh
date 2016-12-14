#!/bin/sh

help() {
	cat << EOF
Run multiple linters.

Usage:
  polylint [-F] [-S]

Options:
  -F  fail on first error
  -S  only run on files that are staged with git

Linters can be configured in a file called .polylintrc in the following format:

    py\tflake8 --exclude tests %s
    js\tjshint
    css,scss\tstylelint "%s"
EOF
}

staged_only=false
fail_early=false

grcode=0

ls_files() {
	if $staged_only; then
		git diff --staged --name-only --diff-filter=ACMR
	else
		git ls-files
	fi | grep "\.\($(echo "$1" | sed 's/,/\\|/g')\)$"
}

run_linter() {
	files=$(ls_files "$1")
	if [ -z "$files" ]; then
		return 0
	fi
	cmd=$(printf "$2" "$files")

	eval $cmd;
	rcode=$?

	if [ $rcode -ne 0 ]; then
		if $fail_early; then
			exit $rcode
		else
			grcode=$rcode
		fi
	fi
}

while getopts hFS flag; do
	case "$flag" in
		(h) help; exit 0;;
		(F) fail_early=true;;
		(S) staged_only=true;;
		(*) exit 1;;
	esac
done

while read line; do
	exts=$(echo "$line" | sed 's/\t.*//')
	cmd=$(echo "$line" | sed 's/^[^\t]*\t//')
	run_linter "$exts" "$cmd"
done < .polylintrc

exit $grcode