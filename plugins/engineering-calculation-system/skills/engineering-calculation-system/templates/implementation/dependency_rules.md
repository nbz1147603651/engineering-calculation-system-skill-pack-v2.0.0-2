# Dependency Rules

Allowed direction:

```text
presentation / report / review / batch / API
  -> books
    -> libraries
      -> core

deployment / release scripts
  -> app entrypoint
    -> books
      -> libraries
        -> core
```

Forbidden reverse dependencies:

```text
core -> libraries/books/UI/report
libraries -> books/UI/report/batch
books -> UI pages or report templates
reports/templates -> engineering formulas
batch -> separate formula logic
deployment -> engineering formulas or module internals
```

Reusable modules must stay asset-ready:

```text
libraries cannot import books, webapp, report, batch, deploy, release, or tests
libraries cannot read environment variables or deployment files
libraries cannot depend on Flask/FastAPI, templates, HTTP requests, or browser state
```
