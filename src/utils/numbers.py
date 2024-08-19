import logging


def only_numbers(text_to_change):
    logging.info('deleting non-digit symbols')
    new_text = ''
    for i in text_to_change:
        if '9' >= i >= '0':
            new_text += i
    if new_text == '':
        return 0
    else:
        return int(new_text)
