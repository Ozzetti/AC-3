import mysql.connector
from mysql.connector import errorcode
from variables import dbpassword

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password=f'{dbpassword}'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `impacta`;")

cursor.execute("CREATE DATABASE `impacta`;")

cursor.execute("USE `impacta`;")

# criando tabelas
TABLES = {}
TABLES['Players'] = ('''
      CREATE TABLE `players` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `categoria` varchar(40) NOT NULL,
      `console` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserindo jogos
players_sql = 'INSERT INTO players (nome, categoria, console) VALUES (%s, %s, %s)'
players = [
      ('Impacta', 'API', 'AC3'),
]
cursor.executemany(players_sql, players)

cursor.execute('select * from impacta.players')
print(' -------------  Players:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()
