Are you tired of getting an error like this when working on TripleO
heat templates?

> Stack CREATE FAILED (overcloud): Resource CREATE failed: The
> Referenced Attribute (BlockStorageServiceChain role_data) is
> incorrect.

It's a lie! What it really means is that somewhere, buried in a nested
stack, you have misspelled a parameter name (or referenced a parameter
that doesn't exist).

The `check-params.py` script will check your templates and flag any
references to parameters that cannot be found in the `parameters`
section of the template.

## Usage:

Use it like this:

    python check-params.py path/to/template1.yaml path/to/template2.yaml ..

Or even:

    find puppet -name '*.yaml' | xargs python check-params.py
