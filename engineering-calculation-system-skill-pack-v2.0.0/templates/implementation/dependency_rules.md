# Dependency Rules

Allowed direction:

```text
presentation / report / review / batch / API
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
```

