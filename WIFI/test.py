from ping3 import ping, verbose_ping


second = ping('www.google.com')*1000
print('it took {} second'.format(second))