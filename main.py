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
    move_to_settings = 'Переход на настройки'
    title = 'Комментарии'
    text_input_password = 'Ввести пароль'
    text_input_name = 'Ввести имя'
    text_settings = 'Настройки'
    name = 'Имя'
    password = 'Пароль'
    translate_fields_menu = [long_field, successfull_reg, user_was, wrong_field, input_password, inputting_chars,
                             delete_chars, input_name, move_to_settings, title, text_input_password,
                             text_input_name, text_settings, name, password]
    entry.run(translate_fields_menu)
