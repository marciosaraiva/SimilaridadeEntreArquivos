import hashlib
import os
import re
from docopt import docopt


def lista_todos_ficheiros(path):
    lista_ficheiros = []

    for root, dirs, files in os.walk(path):
        for file in files:
            #if not "-checkpoint" in file:
            lista_ficheiros.append(os.path.join(root, file).replace("\\", "/"))

    return lista_ficheiros


def detect_mesmo_nome(lista_ficheiros):
    grupos = []

    for ficheiro in lista_ficheiros:
        if len(grupos) == 0:
            grupo = [ficheiro]
            grupos.append(grupo)

        else:
            nao_achou_grupo = True

            for grupo in grupos:
                individuo = grupo[0]
                individuo = individuo.split("/")[-1]
                if ficheiro.split("/")[-1] == individuo:
                    grupo.append(ficheiro)
                    nao_achou_grupo = False

            if nao_achou_grupo:
                grupo = [ficheiro]
                grupos.append(grupo)

    final = []
    for grupo in grupos:
        if len(grupo) > 1:
            final.append(grupo)

    return final


def detect_mesma_extensao(lista_ficheiros):
    grupos = []

    for ficheiro in lista_ficheiros:
        if len(grupos) == 0:
            grupo = [ficheiro]
            grupos.append(grupo)

        else:
            nao_achou_grupo = True

            for grupo in grupos:
                individuo = grupo[0]
                individuo = individuo.split(".")[-1]
                if ficheiro.split(".")[-1] == individuo:
                    grupo.append(ficheiro)
                    nao_achou_grupo = False

            if nao_achou_grupo:
                grupo = [ficheiro]
                grupos.append(grupo)

    final = []
    for grupo in grupos:
        if len(grupo) > 1:
            final.append(grupo)

    return final


def detect_conteudo_binario(lista_ficheiros):
    grupos = []

    for ficheiro in lista_ficheiros:
        if len(grupos) == 0:
            grupo = [ficheiro]
            grupos.append(grupo)

        else:
            nao_achou_grupo = True

            for grupo in grupos:
                individuo = grupo[0]

                ficheiro_individuo = open(individuo, "r")

                ficheiro_temp = open(ficheiro, "r")

                resumo1 = hashlib.md5("".join(ficheiro_temp.readlines()).encode())
                resumo2 = hashlib.md5("".join(ficheiro_individuo.readlines()).encode())

                if resumo1.digest() == resumo2.digest():
                    grupo.append(ficheiro)
                    nao_achou_grupo = False

            if nao_achou_grupo:
                grupo = [ficheiro]
                grupos.append(grupo)

    final = []
    for grupo in grupos:
        if len(grupo) > 1:
            final.append(grupo)

    return final


def detect_regex(lista_ficheiros, pattern):
    grupo = []

    for ficheiro in lista_ficheiros:
        nome = ficheiro.split("/")[-1].split(".")[-2]

        padrao = re.compile(pattern)

        if padrao.match(nome):
            grupo.append(ficheiro)

    return grupo


usage = '''
Expense Tracker CLI.
Usage:
syms.py [-c] [-n] [-e] [<path_directory>]
syms.py [-c] [-n] [-e] [-r <PATTERN>] [<path_directory>]

'''

args = docopt(usage)
print(args)

lista_ficheiros = []
directory_path = os.getcwd()

if not (True in args.values()):
    print("\n Mesmo nome")
    if args['<path_directory>']:
        lista_ficheiros = lista_todos_ficheiros(args['<path_directory>'])
        grupos = detect_mesmo_nome(lista_ficheiros)
        for grupo in grupos:
            print(grupo)
    else:
        directory_path = os.getcwd()
        lista_ficheiros = lista_todos_ficheiros(directory_path+"/")
        grupos = detect_mesmo_nome(lista_ficheiros)
        for grupo in grupos:
            print(grupo)
else:
    if args['-c']:
        print("\n Mesmo conteudo binario")
        if args['<path_directory>']:
            lista_ficheiros = lista_todos_ficheiros(args['<path_directory>'])
            grupos = detect_conteudo_binario(lista_ficheiros)
            for grupo in grupos:
                print(grupo)
        else:
            lista_ficheiros = lista_todos_ficheiros(directory_path+"/")
            grupos = detect_conteudo_binario(lista_ficheiros)
            for grupo in grupos:
                print(grupo)


    if args['-n']:
        print("\n Mesmo nome")
        if args['<path_directory>']:
            lista_ficheiros = lista_todos_ficheiros(args['<path_directory>'])
            grupos = detect_mesmo_nome(lista_ficheiros)
            for grupo in grupos:
                print(grupo)
        else:
            directory_path = os.getcwd()
            lista_ficheiros = lista_todos_ficheiros(directory_path+"/")
            grupos = detect_mesmo_nome(lista_ficheiros)
            for grupo in grupos:
                print(grupo)

    if args['-e']:
        print("\n Mesma extensao")
        if args['<path_directory>']:
            lista_ficheiros = lista_todos_ficheiros(args['<path_directory>'])
            grupos = detect_mesma_extensao(lista_ficheiros)
            for grupo in grupos:
                print(grupo)
        else:
            lista_ficheiros = lista_todos_ficheiros(directory_path+"/")
            grupos = detect_mesma_extensao(lista_ficheiros)
            for grupo in grupos:
                print(grupo)

    if args['-r']:
        print("\n Mesmo padrão")
        if args['<path_directory>']:
            lista_ficheiros = lista_todos_ficheiros(args['<path_directory>'])
            grupos = detect_regex(lista_ficheiros, args['<PATTERN>'])
            for grupo in grupos:
                print(grupo)
        else:
            lista_ficheiros = lista_todos_ficheiros(directory_path+"/")
            grupos = detect_mesma_extensao(lista_ficheiros)
            for grupo in grupos:
                print(grupo)
