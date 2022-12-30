def update_model_field(model, field_name: str, value) -> None:
    if value:
        setattr(model, field_name, value)
    return
