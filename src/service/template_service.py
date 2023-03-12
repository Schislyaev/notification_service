from fastapi import HTTPException, status
from jinja2 import Environment, TemplateSyntaxError, meta

from core.logger import Logger

logger = Logger(__name__)


def validate_template(template: str) -> bool | TemplateSyntaxError:
    """
    Валидация на синтаксис и консистентность шаблона.
    """

    try:
        env = Environment()
        parsed_content = env.parse(template)
    except TemplateSyntaxError as er:
        logger.exception(er)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=er.message
        )

    template_variables = meta.find_undeclared_variables(parsed_content)
    correct_template = ({'first_name', 'second_name'}.issubset(template_variables) and len(template_variables) == 2)
    correct_empty_template = len(template_variables) == 0

    # Разрешаем сообщению быть либо пустым шаблоном без переменных (для ugc), либо содержать имя и фамилию
    if not correct_template and not correct_empty_template:
        logger.exception('Сообщение заполнено не верно')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Шаблон не пустой или не содержит нужные переменные (first_name, second_name)'
        )

    return True
