# coding: utf-8
import abc

from analisadorLexico import *
from analisadorSintatico import *


lista_expSeq, lista_literalSeq, lista_specSeq_retorno, lista_decSeq, lista_varDec, lista_paramSeq, lista_specSeq = [[] for _ in range(7)]
tipo = 0
dicionario_de_simbolos = {}


def atualizaTabela(idd, tipo):
    if not isinstance(idd, list):
        k = []
        k.append(idd)
        idd = k
    for item in idd:
        if item not in dicionario_de_simbolos:
            dicionario_de_simbolos[item] = tipo
        else:
            print('ERRO: Variavel ja foi declarada: ', item)
    print('DICIONARIO DE SIMBOLOS:', dicionario_de_simbolos)
    print('tipo da variavel do dicionario de simbolos', dicionario_de_simbolos[idd[0]])
    return dicionario_de_simbolos[idd[0]]


class Node:
    __metaclass__ = abc.ABCMeta

    def __init__(self, dicionario):
        self.dicionario = dicionario

    @abc.abstractmethod
    def avaliaNo(self):
        pass


class NodeProgram(Node):
    def avaliaNo(self):
        print(self.dicionario)
        self.dicionario['program'].avaliaNo()


class NodeDecSeq(Node):
    def avaliaNo(self):
        print(self.dicionario)
        self.dicionario['dec'].avaliaNo()


class NodeDec(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if len(self.dicionario) == 1:  # variavel
            variavel = self.dicionario['varDec'].avaliaNo()
        elif len(self.dicionario) == 3:  #(procedure)
            print('procedure')
            self.dicionario['paramList'].avaliaNo()
            self.dicionario['block'].avaliaNo()
            atualizaTabela(self.dicionario['ID'], None)
        elif(len(self.dicionario)) == 4:  # função
            print('funcao')
            tipo_funcao = self.dicionario['type'].avaliaNo()
            self.dicionario['paramList'].avaliaNo()
            self.dicionario['block'].avaliaNo()
            atualizaTabela(self.dicionario['ID'], tipo_funcao)


class NodeVarDec(Node):
    def avaliaNo(self):
        global tipo
        print(self.dicionario)
        tipo = self.dicionario['type'].avaliaNo()
        self.dicionario['varSpecSeq'].avaliaNo()


class NodeVarSpecSeq(Node):
    def avaliaNo(self):
        global dicionario_de_simbolos
        global lista_specSeq
        global tipo
        print(self.dicionario)
        lista_specSeq.append(self.dicionario['varSpec'].avaliaNo())
        if 'varSpecSeq' in self.dicionario:
            self.dicionario['varSpecSeq'].avaliaNo()
        else:
            print('tipo das variaveis', tipo)
            print('lista specseq', lista_specSeq)
            atualizaTabela(lista_specSeq, tipo)
            lista_specSeq_retorno = lista_specSeq
            lista_specSeq = []
            return lista_specSeq_retorno


class NodeVarSpec(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if len(self.dicionario) == 1:
            return self.dicionario['ID']
        elif 'literal' in self.dicionario:
            literal = self.dicionario['literal'].avaliaNo()
            if tipo == 'int' and literal != 'int':
                print('DECLAROU INT, CHEGOU OUTRO TIPO: ', type(literal))
            elif tipo == 'string' and literal !='string':
                print('DECLAROU STRING, CHEGOU OUTRO TIPO: ', type(literal))
            elif tipo != literal:
                print('DECLAROU '+ str(tipo)+ ' CHEGOU: ', literal)
            print('meu literal aqui', literal)
            #exit()
            return self.dicionario['ID']
        elif 'NUMBER' in self.dicionario and 'literalSeq' not in self.dicionario:
            return self.dicionario['ID']
        elif 'literalSeq' in self.dicionario:
            print(self.dicionario)
            NUMBER = self.dicionario['NUMBER']
            self.dicionario['literalSeq'].avaliaNo(NUMBER)
            return self.dicionario['ID']


class NodeType(Node):
    def avaliaNo(self):
        print(self.dicionario)
        #print('tipo ', self.dicionario['type'])
        return self.dicionario['type']


class NodeParam(Node):
    def avaliaNo(self):
        print(self.dicionario)
        param_type = self.dicionario['type'].avaliaNo()
        if len(self.dicionario) == 2:
            print({'type': param_type, 'ID': self.dicionario['ID'], 'tipo_var': 'NORMAL'})
        elif len(self.dicionario) == 4:
            print({'type': param_type, 'ID': self.dicionario['ID'], 'tipo_var': 'VETOR'})
        else:
            return "Número de parâmetros do dicionário do sintático está errado."


class NodeBlock(Node):
    def avaliaNo(self):
        print(self.dicionario)
        self.dicionario['varDecList'].avaliaNo()
        self.dicionario['stmtList'].avaliaNo()


class NodeStmt(Node):
    def avaliaNo(self):
        print(self.dicionario)
        self.dicionario['stmt'].avaliaNo()


class NodeIfStmt(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if self.dicionario['exp'].avaliaNo() != 'bool':
            print('ERRO: exp do IFSTMT retornou', self.dicionario['exp'].avaliaNo())
        #exit()
        if len(self.dicionario) == 2:
            self.dicionario['block'].avaliaNo()
        elif len(self.dicionario) == 3:
            self.dicionario['block1'].avaliaNo()
            self.dicionario['block2'].avaliaNo()


class NodeWhileStmt(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if self.dicionario['exp'].avaliaNo() != 'bool':
            print('ERRO exp do no while nao retorna bool')
        self.dicionario['block'].avaliaNo()


class NodeForStmt(Node):
    def avaliaNo(self):
        print(self.dicionario)
        variavel1 = self.dicionario['assign1'].avaliaNo()
        variavel2 = self.dicionario['assign2'].avaliaNo()
        if self.dicionario['exp'].avaliaNo() != 'bool':
            print('ERRO: exp do nó FOR não retorna "bool"')
        self.dicionario['block'].avaliaNo()


class NodeBreakStmt(Node):
    def avaliaNo(self):
        print(self.dicionario)
        # Verificar escopo do break, alterar escopo após break.


class NodeReadStmt(Node):
    def avaliaNo(self):
        print(self.dicionario)
        print('read')

        self.dicionario['var'].avaliaNo()


class NodeWriteStmt(Node):
    def avaliaNo(self):
        print(self.dicionario)
        self.dicionario['expList'].avaliaNo()


class NodeReturnStmt(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if 'exp' in self.dicionario:
            self.dicionario['exp'].avaliaNo()
        '''
        escopo = verifica_escopo_return()
        if escopo == False:
            return 'return não está dentro de um subprograma'
        if escopo == 'funcao':
            tipo_retorno_exp = self.dicionario['exp'].avaliaNo()
            avalia_tipo_retorno_com_declaracao(tipo_retorno_exp)
        if escopo == 'procedimento':
            if 'exp' in self.dicionario:
                return 'retorno de exp dentro de procedimento ERRO.'
        '''

class NodeSubCall(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if self.dicionario['ID'] not in dicionario_de_simbolos:
            print('ERRO: Subcall'+self.dicionario['ID']+'() não declarada.')
            return None
        self.dicionario['expList'].avaliaNo()
        return dicionario_de_simbolos[self.dicionario['ID']]


class NodeAssign(Node):
    def avaliaNo(self):
        print(self.dicionario)
        tipo_variavel_assign = self.dicionario['var'].avaliaNo()  # variável está na TS, verifica se exp está correto.
        tipo_exp = self.dicionario['exp'].avaliaNo()
        if tipo_variavel_assign != tipo_exp:
            print('ATRIBUIÇÃO ENTRE TIPOS INCOMPATIVEIS: '+str(tipo_exp)+str(tipo_variavel_assign))
        return tipo_exp


class NodeExpArithimetic(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if self.dicionario['exp1'].avaliaNo() == self.dicionario['exp2'].avaliaNo() and self.dicionario['exp1'].avaliaNo() == 'int': # verifica o tipo, retorno disso eh number, string, etc...
            return 'int'
        else:
            print('ERRO: Operação aritimetica entre tipos de variáveis diferentes '+ self.dicionario['exp1'].avaliaNo()+self.dicionario['exp2'].avaliaNo())


class NodeExpComparison(Node):
    def avaliaNo(self):
        print(self.dicionario)
        print('OPERADOR DE COMPARAÇÃO', self.dicionario['op'])
        op = self.dicionario['op']
        var_tipo1 = self.dicionario['exp1'].avaliaNo()
        var_tipo2 = self.dicionario['exp2'].avaliaNo()
        if var_tipo1 != var_tipo2:  # Verifica se operandos são do mesmo tipo
            print('COMPARAÇÃO ENTRE VARIAVEIS DE TIPOS DIFERENTES: '+var_tipo1+' '+var_tipo2)
            return None
        if (op != '!=' and op != '==') and (var_tipo1 != 'int' or var_tipo2 != 'int'):  # Verifica se relacional eh (>,<,>=,<=) e se operandos são do tipo 'int'
            print('RELACIONAL ENTRE TIPOS NÃO INTEIROS: '+var_tipo1+' '+var_tipo2)
            return None
        print('var_tipo1: ', var_tipo1)
        print('var_tipo2: ', var_tipo2)
        return 'bool'


class NodeExpLogic(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if len(self.dicionario) == 3:
            if self.dicionario['exp1'].avaliaNo() == self.dicionario['exp2'].avaliaNo() and self.dicionario['exp1'].avaliaNo() == 'bool':
                return 'bool'
            else:
                print('ERRO: Expressão lógica entre tipos diferentes'+ str(self.dicionario['exp1'].avaliaNo())+ str(self.dicionario['exp2'].avaliaNo()))
                return None
        if 'NOT' in self.dicionario:
            if self.dicionario['exp'].avaliaNo() == 'bool':
                return 'bool'
            else:
                return 'ERRO: Negação de uma expressão que não retorna um booleano'
        if 'UMINUS' in self.dicionario:
            if self.dicionario['exp'].avaliaNo() == 'int':
                return 'bool'
            else:
                return 'ERRO: Esperava-se um inteiro depois de UMINUS e retornou '+self.dicionario['exp'].avaliaNo()



class NodeExpTernary(Node):
    def avaliaNo(self):
        print(self.dicionario)
        exp1 = self.dicionario['exp1'].avaliaNo()
        exp2 = self.dicionario['exp2'].avaliaNo()
        exp3 = self.dicionario['exp3'].avaliaNo()
        if exp1 != 'bool':
            print('ERRO: exp1 retornou: '+str(exp1)+' esperava-se um booleano')
        if exp2 != exp3:
            print('ERRO: exp2 <> exp3 Operador Ternário')


class NodeExpSubCall(Node):
    def avaliaNo(self):
        self.dicionario['subCall'].avaliaNo()


class NodeExpVar(Node):
    def avaliaNo(self):
        return self.dicionario['var'].avaliaNo()


class NodeExpLiteral(Node):
    def avaliaNo(self):
        return self.dicionario['literal'].avaliaNo()


class NodeExpMultParent(Node):
    def avaliaNo(self):
        print(self.dicionario)
        self.dicionario['exp'].avaliaNo()


class NodeVar(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if self.dicionario['ID'] not in dicionario_de_simbolos:
            print('ERRO: Variavel '+self.dicionario['ID']+' nao foi declarada')
            atualizaTabela(self.dicionario['ID'], None)
        return dicionario_de_simbolos[self.dicionario['ID']]


class NodeLiteral(Node):
    def avaliaNo(self):
        print(self.dicionario)
        literal = self.dicionario['literal']
        print('LITERAL: ', literal)
        if self.dicionario['literal'] == 'true' or self.dicionario['literal'] == 'false':
            return 'bool'
        elif type(self.dicionario['literal']).__name__ == 'int':
            return 'int'
        elif type(self.dicionario['literal']).__name__ == 'str':
            return 'string'


class NodeParamList(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if self.dicionario['paramSeq'] == None:
            return []
        else:
            return self.dicionario['paramSeq'].avaliaNo()


class NodeParamSeq(Node):
    def avaliaNo(self):
        print(self.dicionario)
        global lista_paramSeq
        lista_paramSeq.append(self.dicionario['param'].avaliaNo())
        if 'paramSeq' in self.dicionario:
            self.dicionario['paramSeq'].avaliaNo()
        else:
            lista_paramSeq_retorno = lista_paramSeq
            lista_paramSeq = []
            return lista_paramSeq_retorno


class NodeVarDecList(Node):
    def avaliaNo(self):
        print(self.dicionario)
        global lista_varDec
        if 'empty' in self.dicionario:
            lista_varDec_retorno = lista_varDec
            return lista_varDec_retorno
        if 'varDecList' in self.dicionario:
            lista_varDec.append(self.dicionario['varDec'].avaliaNo())
            self.dicionario['varDecList'].avaliaNo()


class NodeDecSeq(Node):
    def avaliaNo(self):
        print(self.dicionario)
        global lista_decSeq
        lista_decSeq.append(self.dicionario['dec'].avaliaNo())
        if 'decSeq' in self.dicionario:
            self.dicionario['decSeq'].avaliaNo()
        else:
            lista_decSeq_retorno = lista_decSeq
            lista_decSeq = []
            return lista_decSeq_retorno


class NodeStmtList(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if 'empty' in self.dicionario:
            return
        self.dicionario['stmt'].avaliaNo()
        if self.dicionario['stmtList'] != None:
            self.dicionario['stmtList'].avaliaNo()  # Avalia o stmtList


class NodeLiteralSeq(Node):
    def avaliaNo(self, NUMBER):
        global lista_literalSeq
        global tipo
        print(self.dicionario)
        lista_literalSeq.append(self.dicionario['literal'].avaliaNo())
        if 'literalSeq' in self.dicionario:
            self.dicionario['literalSeq'].avaliaNo(NUMBER)
        else:
            if len(lista_literalSeq) != NUMBER:
                print('ERRO: Tamanho do vetor <> do tamanho declarado: '+str(len(lista_literalSeq))+ ' <> '+str(NUMBER))
            print("LISTA LITERAL SEQ TESTE ", lista_literalSeq)
            if tipo == 'int':
                for item in lista_literalSeq:
                    if item != 'int':
                        print('TIPO DO VETOR ERA PRA SER INT, VEIO'+ str(item))
            if tipo == 'string':
                for item in lista_literalSeq:
                    print(item)
                    if item != 'string':
                        print('TIPO DO VETOR ERA PRA SER STR, VEIO '+ str(item))
            if tipo == 'bool':
                for item in lista_literalSeq:
                    if item != 'bool':
                        print('TIPO DO VETOR ERA PRA SER BOOL, VEIO: ', str(item))
            #exit()
            lista_literalSeq_retorno = lista_literalSeq
            lista_literalSeq = []
            return lista_literalSeq_retorno


class NodeExpList(Node):
    def avaliaNo(self):
        print(self.dicionario)
        if 'empty' in self.dicionario:
            return []
        else:
            self.dicionario['expSeq'].avaliaNo()


class NodeExpSeq(Node):
    def avaliaNo(self):
        print(self.dicionario)
        global lista_expSeq
        lista_expSeq.append(self.dicionario['exp'].avaliaNo())
        if 'expSeq' in self.dicionario:
            self.dicionario['expSeq'].avaliaNo()
        else:
            lista_expSeq_retorno = lista_expSeq
            lista_expSeq = []
            return lista_expSeq_retorno


class NodeEmpty(Node):
	def avaliaNo(self):
		pass
