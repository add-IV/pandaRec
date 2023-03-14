# Defining how to store recipes

## Recipe

- id: int
- name: str
- description: str
- code: str
- keywords: str

## Filetype

- json: too verbose, not human readable
- yaml: seems to be the best option
- toml: more verbose than yaml, array of object especially verbose

proposed format:

```yaml
recipes:
  - id: 1
    name: "rename columns"
    description: "rename columns"
    code: "tbd"
    keywords: "tbd"
  - id: 2
    name: "drop columns"
    description: "drop columns"
    code: "tbd"
    keywords: "tbd"
```

Seems reasonable until we have an absurd amount of recipes. How many recipes are possible should be investigated.

## Refering to a recipe with name or id

Both are possible, if we refer to a recipe with name, we need to make sure that the name is unique.
If we refer to a recipe with id, then removing a recipe is complicated without creating holes in the numbering.

## Code

Using [Vscode Snippets](https://code.visualstudio.com/docs/editor/userdefinedsnippets) as basis.

[EBNF](https://en.wikipedia.org/wiki/Extended_Backus-Naur_form) for VSC snippets:

```ebnf
any = tabstop | placeholder | choice | variable | text
tabstop     ::= '$' int
                | '${' int '}'
                | '${' int  transform '}'
placeholder ::= '${' int ':' any '}'
choice      ::= '${' int '|' text (',' text)* '|}'
variable    ::= '$' var | '${' var '}'
                | '${' var ':' any '}'
                | '${' var transform '}'
transform   ::= '/' regex '/' (format | text)+ '/' options
format      ::= '$' int | '${' int '}'
                | '${' int ':' '/upcase' | '/downcase' | '/capitalize' | '/camelcase' | '/pascalcase' '}'
                | '${' int ':+' if '}'
                | '${' int ':?' if ':' else '}'
                | '${' int ':-' else '}' | '${' int ':' else '}'
regex       ::= JavaScript Regular Expression value (ctor-string)
options     ::= JavaScript Regular Expression option (ctor-options)
var         ::= [_a-zA-Z] [_a-zA-Z0-9]*
int         ::= [0-9]+
text        ::= .*
if          ::= text
else        ::= text
```

Changes to be made:

- automatically add the right rows and columns to the snippet.
- get rid of unnecessary parts of the EBNF.

## Autogenerating recipes

Could scrape the pandas documentation and generate recipes from there.

## Keywords

Possibly autogenerated.