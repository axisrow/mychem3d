def print_bytes_with_highlights(byte_array, highlights):
    # ANSI-коды для красного цвета и сброса
    red = '\033[91m'
    end = '\033[0m'
    
    # Создание множества для быстрого поиска выделяемых индексов
    highlight_indices = set()
    for offset, n in highlights:
        if offset < 0 or offset >= len(byte_array):
            print(f"Ошибка: смещение {offset} вне диапазона.")
            return
        if n < 0 or offset + n > len(byte_array):
            print(f"Ошибка: количество байтов {n} для смещения {offset} вне диапазона.")
            return
        highlight_indices.update(range(offset, offset + n))

    # Вывод байтов с выделением
    for i in range(len(byte_array)):
        if i in highlight_indices:
            print(f"{red}{byte_array[i]:02x}{end}", end=' ')
        else:
            print(f"{byte_array[i]:02x}", end=' ')
    
    print()  # Переход на новую строку после вывода

# Пример использования
byte_array = bytearray([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09])
highlights = [(2, 3), (6, 2)]
print_bytes_with_highlights(byte_array, highlights)