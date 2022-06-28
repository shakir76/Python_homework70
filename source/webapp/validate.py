def article_validate(title, author, content):
    errors = {}
    if not title:
        errors["title"] = "Поле обязательное"
    elif len(title) > 50:
        errors["title"] = "Должно быть меньше 50 символов"
    if not author:
        errors["author"] = "Поле обязательное"
    elif len(author) > 50:
        errors["author"] = "Должно быть меньше 50 символов"
    if not content:
        errors["content"] = "Поле обязательное"
    elif len(content) > 3000:
        errors["content"] = "Должно быть меньше 3000 символов"
    return errors
