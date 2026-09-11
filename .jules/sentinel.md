## 2025-05-15 - XSS in Report Template Tags
**Vulnerability:** XSS in `internal_link` and `render_html_text` report template tags due to use of `mark_safe` with unescaped user input.
**Learning:** `mark_safe` should only be used on strings where you are absolutely sure the content is safe. When combining HTML templates with user input, `format_html` is much safer as it automatically escapes arguments.
**Prevention:** Always use `format_html` instead of `mark_safe` with f-strings when generating HTML with dynamic content.
