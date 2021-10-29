from vkbottle.bot import Blueprint, Message
from classes.abstract_command import AbstractCommand
import json
from typing import Optional
from os import popen
import pyparsing as pyp
import math
import operator

class NumericStringParser(object):
    def pushFirst(self, strg, loc, toks ):
        self.exprStack.append( toks[0] )
    def pushUMinus(self, strg, loc, toks ):
        if toks and toks[0] == '-':
            self.exprStack.append( 'unary -' )
    def __init__(self):
        point = pyp.Literal( "." )
        e     = pyp.CaselessLiteral( "E" )
        fnumber = pyp.Combine( pyp.Word( "+-"+pyp.nums, pyp.nums ) + 
                           pyp.Optional( point + pyp.Optional( pyp.Word( pyp.nums ) ) ) +
                           pyp.Optional( e + pyp.Word( "+-"+pyp.nums, pyp.nums ) ) )
        ident = pyp.Word(pyp.alphas, pyp.alphas+pyp.nums+"_$")       
        plus  = pyp.Literal( "+" )
        minus = pyp.Literal( "-" )
        mult  = pyp.Literal( "*" )
        div   = pyp.Literal( "/" )
        lpar  = pyp.Literal( "(" ).suppress()
        rpar  = pyp.Literal( ")" ).suppress()
        addop  = plus | minus
        multop = mult | div
        expop = pyp.Literal( "^" )
        pi    = pyp.CaselessLiteral( "PI" )
        expr = pyp.Forward()
        atom = ((pyp.Optional(pyp.oneOf("- +")) +
                 (pi|e|fnumber|ident+lpar+expr+rpar).setParseAction(self.pushFirst))
                | pyp.Optional(pyp.oneOf("- +")) + pyp.Group(lpar+expr+rpar)
                ).setParseAction(self.pushUMinus)       
        factor = pyp.Forward()
        factor << atom + pyp.ZeroOrMore( ( expop + factor ).setParseAction(
            self.pushFirst ) )
        term = factor + pyp.ZeroOrMore( ( multop + factor ).setParseAction(
            self.pushFirst ) )
        expr << term + pyp.ZeroOrMore( ( addop + term ).setParseAction( self.pushFirst ) )
        self.bnf = expr
        epsilon = 1e-12
        self.opn = { "+" : operator.add,
                "-" : operator.sub,
                "*" : operator.mul,
                "/" : operator.truediv,
                "^" : operator.pow }
        self.fn  = { "sin" : math.sin,
                "cos" : math.cos,
                "tan" : math.tan,
                "factorial" : math.factorial,
                "fact" : math.factorial,
                "abs" : abs,
                "trunc" : lambda a: int(a),
                "round" : round,
                "sgn" : lambda a: abs(a)>epsilon and ((a > 0) - (a < 0)) or 0}
        self.exprStack = []
    def evaluateStack(self, s ):
        op = s.pop()
        if op == 'unary -':
            return -self.evaluateStack( s )
        if op in "+-*/^":
            op2 = self.evaluateStack( s )
            op1 = self.evaluateStack( s )
            return self.opn[op]( op1, op2 )
        elif op == "PI":
            return math.pi 
        elif op == "E":
            return math.e  
        elif op in self.fn:
            return self.fn[op]( self.evaluateStack( s ) )
        elif op[0].isalpha():
            return 0
        else:
            return float( op )
    def eval(self, num_string, parseAll = True):
        self.exprStack = []
        results = self.bnf.parseString(num_string, parseAll)
        val = self.evaluateStack( self.exprStack[:] )
        return val

nsp = NumericStringParser()

bp = Blueprint()

config = 'config.json'

def config_load(config):
    with open(config, 'r') as f:
        return json.load(f)

class Command(AbstractCommand):
    def __init__(self):
        super().__init__(handler = ['/e <item>', '/E <item>'], description = 'exec neofetch, uptime, time, mem, ip, calc')

e = Command()

@bp.on.message(text=e.hdl())
async def ex(m: Message, item: Optional[str] = None):
    data = config_load(config)
    super_admin = data["super_admin"]
    
    if ('/E' == m.text[:2]):
        up = True
    else:
        up = False

    item = item.lower()
    
    try:
        if (item == 'neofetch'):
            await e.ans_up((popen('neofetch --disable shell --stdout').read()), m)

        elif (item == 'uptime'):
            await e.ans_up((popen('neofetch uptime | cut -c9-').read()), m)

        elif (item == 'time'):
            await e.ans_up((popen('date +"%H:%M %d/%m/%Y"').read()), m)

        elif (item == 'mem'):
            await e.ans_up((popen('neofetch memory | cut -c9-').read()), m)

        elif (item == 'ip' and m.from_id == super_admin):
            await e.ans_up((popen('curl -s checkip.amazonaws.com').read()), m)

        elif (item[:5] == 'calc '):
            item = item[5:]
            await e.ans_up(nsp.eval(item), m)

        # elif (m.from_id == super_admin):
        #     await e.ans_up((popen(str(item)).read()), m)

    except Exception as err:
        await e.ans_up(err, m)
    