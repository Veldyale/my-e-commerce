from django import template
from django.utils.safestring import mark_safe
from mainapp.models import Smartphone

register = template.Library()


TABLE_HEAD = """
                <table class="table">
                  <tbody>
             """

TABLE_TAIL = """
                  </tbody>
                </table>
             """

TABLE_CONTENT = """
                <tr>
                  <th scope="row"></th>
                  <td>{name}</td>
                  <td>{value}</td>
                </tr>
             """

PRODUCT_SPEC = {
      'notebook': {
          'Диагональ:': 'diagonal',
          'Тип матрицы дисплея:': 'display_type',
          'Частота процессора:': 'processor_freq',
          'Оперативная память:': 'ram',
          'Видеокарта:': 'video',
          'Время работы от аккумулятора:': 'time_without_charge'
      },
      'smartphone': {
          'Диагональ:': 'diagonal',
          'Тип матрицы дисплея:': 'display_type',
          'Разрешение экрана:': 'resolution',
          'Объем батареи:': 'accum_volume',
          'Оперативная память:': 'ram',
          'Поддержка карт памяти:': 'sd',
          'Максимальный объем карты памяти:': 'sd_volume_max',
          'Основная камера:': 'main_cam_mp',
          'Фронтальная камера:': 'frontal_cam_mp'
      }
}


def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content

@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    if isinstance(product, Smartphone):
        if not product.sd:
            PRODUCT_SPEC['smartphone'].pop('Максимальный объем карты памяти:')
            # PRODUCT_SPEC['smartphone']['Поддержка карт памяти:'] = '1'
        else:
            # PRODUCT_SPEC['smartphone']['Поддержка карт памяти:'] = '2'
            PRODUCT_SPEC['smartphone']['Максимальный объем карты памяти:'] = 'sd_volume_max'
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)