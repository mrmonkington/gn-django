
def get_form_error_dict(form):
    """
    Given a django form, collect the errors in to a string: string mapping.
    A normal form error dictionary will have a list of errors for each value.

    Args:
      * `form` - Form - the form with errors

    Returns:
      A string:string dictionary with keys as form fields and values as a comma
      delimited string of error messages.
    """
    errors = {f_name: ', '.join([val.strip('.') for val in values]) 
        for f_name, values in form.errors.items()}
    return errors

