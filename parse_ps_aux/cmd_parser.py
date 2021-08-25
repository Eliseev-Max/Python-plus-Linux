import subprocess as sp
import time
from collections import defaultdict


MAX_CPU = 0.0
MAX_MEM = 0.0
TOTAL_MEM = 0.0
TOTAL_CPU = 0.0
ps_result = []
user_proc = defaultdict(int)
filename = f"{time.strftime('%Y-%m-%d-%H:%M')}-scan.txt"


def handle_ps_aux():
    """
    Функция преобразует вывод команды ps aux, полученый в результате работы функции run
    модуля subprocess в список.
    Каждый элемент полученного списка является списком подстрок - значений колонок:
    USER | PID | %CPU | %MEM | VSZ | RSS | TTY | STAT | START | TIME | COMMAND
    для каждой последующей строки вывода команды ps aux

    """
    result = sp.run(["ps", "aux"], stdout=sp.PIPE, stderr=sp.PIPE, encoding='utf-8')
    for i in result.stdout.split('\n'):
        if i.split(None, 10) != []:
            ps_result.append(i.split(None, 10))
    return ps_result[1:]


for elem in handle_ps_aux():
    user_proc[elem[0]] +=1
    TOTAL_MEM += float(elem[4])
    TOTAL_CPU += float(elem[2])
    if MAX_CPU < float(elem[2]):
        MAX_CPU = float(elem[2])
        process_using_max_cpu = elem

    if MAX_MEM < float(elem[3]):
        MAX_MEM = float(elem[3])
        process_using_max_mem = elem

system_users = '\n\t'.join((user_proc.keys()))
report_general = (
    "Отчёт о состоянии системы:\n"
    f"Пользователи системы:\n\t{system_users}\n"
    f"Всего процессов запущено: {len(handle_ps_aux())}\n"
    f"Всего памяти используется: {int(TOTAL_MEM / 1000)} Мб\n"
    f"Всего CPU используется: {round(TOTAL_CPU,2)} %\n"
    "Пользовательских процессов:\n"
)
report_individual = (
    f"\nБольше всего памяти использует:\n\tUSER: {process_using_max_mem[0]}\n"
    f"\tPID: {process_using_max_mem[1]}\n"
    f"\t%MEM({MAX_MEM} %)\n"
    f"Больше всего CPU использует:\n\tUSER: {process_using_max_cpu[0]}\n"
    f"\tPID: {process_using_max_cpu[1]}\n"
    f"\t%CPU({MAX_CPU} %)"
)

for key in user_proc:
    report_general += f"\tПользователь {key}:\t\tзапущено процессов: {user_proc[key]}\n "

report = report_general + report_individual

with open(filename, 'w+', encoding='utf-8') as f:
    f.write(report)

print(report)
