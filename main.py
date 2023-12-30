from Entrance import Enter


def return_entry():
    return entry


if __name__ == "__main__":
    entry = Enter(False)
    entry.append_block_menu('Имя')
    entry.append_block_menu('Пароль')
    entry.append_block_menu('Настройки')
    long_field = 'Слишком длинное поле'
    successfull_reg = 'Вы успешно зарегистрировались'
    user_was = 'Пользователь с таким именем уже существует'
    wrong_field = 'Имя или пароль введены неверно'
    input_password = 'Переключились на введение пароля'
    inputting_chars = 'Вводятся символы'
    delete_chars = 'Удаляются символы'
    input_name = 'Переключение на введение имени'
    settings = 'Переход на настройки'
    translate_fields_menu = []
    translate_fields_menu.append(long_field)
    translate_fields_menu.append(successfull_reg)
    translate_fields_menu.append(user_was)
    translate_fields_menu.append(wrong_field)
    translate_fields_menu.append(input_password)
    translate_fields_menu.append(inputting_chars)
    translate_fields_menu.append(delete_chars)
    translate_fields_menu.append(input_name)
    translate_fields_menu.append(settings)
    entry.run(translate_fields_menu)
